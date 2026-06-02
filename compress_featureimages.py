"""
压缩 featureimages 目录下的图片到约 200KB。

用法: python compress_featureimages.py
"""

import os
from pathlib import Path
from PIL import Image

TARGET_SIZE = 200 * 1024  # 200KB
PROJECT_ROOT = Path(__file__).parent
DIRS = [
    PROJECT_ROOT / "medias" / "featureimages",
    PROJECT_ROOT / "hexo-source" / "themes" / "hexo-theme-matery" / "source" / "medias" / "featureimages",
]


def compress_to_target(img_path, target_bytes=TARGET_SIZE):
    """将图片压缩到目标大小左右（二分法调整 quality）"""
    img = Image.open(img_path)
    if img.mode == "RGBA":
        img = img.convert("RGB")

    # 先尝试直接缩放到合理尺寸再压质量
    w, h = img.size
    # 如果宽度超过 1280px，先缩放
    max_w = 1280
    if w > max_w:
        ratio = max_w / w
        img = img.resize((max_w, int(h * ratio)), Image.LANCZOS)

    lo, hi = 10, 95
    best_data = None
    while lo <= hi:
        mid = (lo + hi) // 2
        img.save(img_path, "JPEG", quality=mid, optimize=True)
        size = img_path.stat().st_size
        if size <= target_bytes:
            best_data = mid
            lo = mid + 1  # 还能再提高质量
        else:
            hi = mid - 1
    # 用最佳 quality 重新保存
    if best_data is not None:
        img.save(img_path, "JPEG", quality=best_data, optimize=True)
    return img_path.stat().st_size


def main():
    total_saved = 0
    for d in DIRS:
        if not d.exists():
            print(f"跳过（不存在）: {d}")
            continue
        for f in sorted(d.glob("*.jpg")):
            old_size = f.stat().st_size
            new_size = compress_to_target(f)
            saved = old_size - new_size
            total_saved += saved
            print(f"  {f.name}: {old_size // 1024}KB -> {new_size // 1024}KB (省 {(old_size - new_size) // 1024}KB)")

    print(f"\n完成！总共节省 {total_saved // 1024 // 1024}MB")


if __name__ == "__main__":
    main()
