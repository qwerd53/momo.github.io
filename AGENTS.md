# AGENTS.md

本文件为 AI 编码代理（Claude Code / CodeArts 等）在此仓库中工作时提供指引。

## 仓库概述

基于 **hexo-theme-matery** 主题的个人技术博客（Hexo 6 静态站点）。`hexo-source/` 目录是 Hexo 源码（唯一需要维护的源），仓库根目录是构建后生成的静态 HTML，由 GitHub Pages 直接托管，**不要手动修改根目录的生成产物**。

## 写文章流程

1. 进入 `hexo-source/` 目录
2. 在 `source/_posts/` 下新建 `.md` 文件
3. 运行 `./build.sh` 构建
4. 提交并推送

## 目录结构

```
/
├── hexo-source/                       # Hexo 源码（唯一源码目录）
│   ├── _config.yml                    # Hexo 根配置
│   ├── package.json                   # 依赖清单
│   ├── scaffolds/                     # 新建文章/页面的脚手架模板
│   ├── themes/hexo-theme-matery/      # Matery 主题（定制版）
│   │   ├── _config.yml                # 主题配置（菜单、音乐、评论、社交）
│   │   ├── layout/                    # EJS 页面模板与 _partial 局部组件
│   │   ├── source/                    # 主题 css/js/libs/medias 静态资源
│   │   ├── scripts/tags/              # 自定义 Hexo 标签插件
│   │   └── languages/                 # 多语言文案（zh-CN/zh-HK/jp/default）
│   └── source/
│       ├── _posts/                    # 博客文章（Markdown）
│       ├── about/index.md             # 关于页
│       ├── friends/index.md           # 友情链接页
│       ├── contact/index.md           # 留言板页
│       ├── tags/index.md              # 标签页
│       ├── categories/index.md        # 分类页
│       ├── 404/index.md               # 404 页
│       └── medias/                    # 站点图片（avatar.jpg、logo.jpg）
├── compress_featureimages.py          # 配图压缩脚本（Pillow）
├── download_pexels.py                 # Pexels 素材下载脚本
├── index.html                         # [生成] 首页
├── about/ archives/ categories/ ...   # [生成] 各页面
├── css/ js/ libs/ medias/             # [生成] 静态资源
└── build.sh                           # 一键构建脚本
```

## 关键配置文件

| 文件 | 用途 |
|---|---|
| `hexo-source/_config.yml` | Hexo 根配置（URL、分页、插件、主题选择） |
| `hexo-source/themes/hexo-theme-matery/_config.yml` | 主题配置（菜单、音乐、评论、社交、外观） |
| `hexo-source/source/_posts/*.md` | 博客文章 |
| `hexo-source/source/medias/` | 头像/Logo 等站点图片 |
| `hexo-source/source/friends/index.md` | 友情链接页 |
| `.env` | 环境变量（Pexels API Key、Gitalk 凭证），**已忽略，勿提交** |
| `build.sh` | 一键构建脚本 |

## 常用操作

### 本地调试

启动本地服务器进行预览和测试（修改代码后会自动重新加载）：

```bash
cd hexo-source
npx hexo server
```

访问 `http://localhost:4000/momo.github.io/` 查看效果。按 `Ctrl+C` 停止服务器。

### 写文章
```bash
cd hexo-source
hexo new "文章标题"          # 创建新文章
# 编辑 source/_posts/文章标题.md
cd .. && bash build.sh       # 构建并部署
```

文章文件名使用中文标题，需在 frontmatter 填写 `title`、`date`、`categories`、`tags`。

### 辅助脚本

```bash
python compress_featureimages.py   # 将 featureimages 背景图压缩到约 200KB
python download_pexels.py          # 从 Pexels 下载风景图替换 banner/featureimages（需 .env 中 PEXELS_API_KEY）
```

### 添加音乐
编辑 `hexo-source/themes/hexo-theme-matery/_config.yml` 中的 `music` 部分：
- `server`: 音乐平台（netease/tencent/kugou/xiami/baidu）
- `type`: 类型（playlist/song/album）
- `id`: 歌单/歌曲 ID

### 添加友链
编辑 `hexo-source/source/friends/index.md`。

### 修改社交链接
编辑主题配置中的 `socialLink` 部分。

### 修改网站标题/描述
编辑 `hexo-source/_config.yml` 中的 `title`、`subtitle`、`description`。

### 修改头像/Logo
- 头像：替换 `hexo-source/source/medias/avatar.jpg`
- Logo：替换 `hexo-source/source/medias/logo.jpg`
- Favicon：替换 `hexo-source/source/favicon.jpg`
- 路径需在主题配置中设置 `/momo.github.io/` 前缀

## 构建脚本说明

`build.sh` 执行以下步骤：
1. 加载 `.env` 环境变量（供凭证引用）
2. `hexo clean` — 清理旧的生成文件
3. `hexo generate` — 生成静态文件到 `hexo-source/public/`
4. 删除根目录旧的生成产物，复制 `hexo-source/public/*` 到项目根目录

## 项目知识库（Wiki）

本仓库已生成结构化 Wiki，位于 `.codeartsdoer/.codebase/branches/main/docs/`：

- `codebase-knowledge/index.md` — 模块树导航（站点配置、博客内容、主题模板/资源/配置、工具脚本）
- `project-knowledge/index.md` — 全仓规范索引（构建、配置、日志、异常、依赖、业务术语、前端风格、外部依赖）
- `WikiRetrieval.md` — Wiki 检索使用指南
- `overview.md` — 知识库总览

修改代码后如需同步知识库，可使用 `repo-simple-wiki-update` 流程增量更新。

## 主题更新

主题 `hexo-source/themes/hexo-theme-matery/` 是**定制过**的版本（内含独立 `.git`），一般不建议直接覆盖更新。

从官方仓库克隆最新主题：
```bash
cd hexo-source/themes
rm -rf hexo-theme-matery
git clone https://github.com/blinkfox/hexo-theme-matery.git
```

更新后需要迁移原有配置（favicon、logo、social link、music 等）。

## 部署方式

推送到 GitHub 后，GitHub Pages 自动部署 `main` 分支的静态文件。

```bash
git add -A
git commit -m "更新说明"
git push
```

## URL 路径规则

本项目部署在 `https://qwerd53.github.io/momo.github.io/`，所有资源路径需要 `/momo.github.io/` 前缀：
- favicon: `/momo.github.io/favicon.jpg`
- logo: `/momo.github.io/medias/logo.jpg`
- 图片: `/momo.github.io/medias/xxx.jpg`

> 注意：`.env` 含敏感凭证，已在 `.gitignore` 中忽略，切勿提交或写入文档。