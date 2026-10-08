---
title: 为 Hexo 博客添加 Gitalk 评论系统：从配置到排错
date: 2026-10-08 10:30:40
author: qwerd53
categories: 博客搭建
tags:
  - Hexo
  - Gitalk
  - 评论系统
summary: 为 Hexo 博客接入 Gitalk 评论系统，从创建 GitHub OAuth App、主题配置，到首次初始化与常见问题排错。
---

## 前言

Hexo 博客搭好、部署完成之后，评论功能通常是比较容易被补上的一块。Gitalk 的思路比较简单：评论不需要自己搭数据库，而是直接借助 GitHub Issues 保存，再通过 GitHub OAuth 完成登录。

如果你的博客本身就部署在 GitHub Pages 上，这种方案尤其方便。下面以 Fluid 主题为例，从创建 GitHub OAuth App 开始，把 Gitalk 的配置、部署、首次初始化以及几个容易踩坑的地方一起走一遍。

## 为什么用 Gitalk

Gitalk 的几个特点比较适合技术博客：

- **免费**：评论数据放在 GitHub Issues 中，不需要单独购买评论服务。
- **不需要后端**：评论区本身通过前端调用 GitHub API 工作。
- **支持 Markdown**：评论里可以使用 Markdown，也可以插入代码。
- **GitHub 登录**：读者直接使用 GitHub 账号登录。
- **数据自己掌握**：评论实际对应的是自己 GitHub 仓库中的 Issue。
- **和技术博客比较搭**：登录、评论和 Issue 管理都围绕 GitHub 展开。

当然，它也有一个前提：读者需要有 GitHub 账号。如果你的博客面向的主要就是开发者，这个限制通常不算大。

## 最后会得到什么

配置完成后，每篇开启评论的文章底部都会出现 Gitalk 评论区。

读者可以：

- 使用 GitHub 账号登录；
- 在文章下发表评论；
- 使用 Markdown 编写评论；
- 直接在 GitHub Issues 中查看和管理评论。

第一次使用某篇文章时，需要由管理员初始化对应的 Issue。初始化完成后，后续评论就会直接写入这个 Issue。

## 开始之前

需要准备的东西不多：

- 一个已经搭好的 Hexo 博客；
- 本文以 Fluid 主题为例；
- 博客已经部署到 GitHub Pages；
- 一个 GitHub 账号。

如果这些都已经准备好了，可以直接开始配置。

## 一、创建 GitHub OAuth App

Gitalk 使用 GitHub OAuth 完成用户登录，所以第一步要先创建一个 OAuth App。

### 1. 打开 GitHub 的 OAuth App 设置

登录 GitHub 后，可以直接打开：

```
https://github.com/settings/applications/new
```

也可以从 GitHub 页面进入：

```
GitHub 头像 → Settings → Developer settings → OAuth Apps → New OAuth App
```

### 2. 填写 OAuth App 信息

创建页面会要求填写几个字段。下面使用占位符表示需要填写自己的信息：

| 字段 | 填写内容 | 示例 |
| --- | --- | --- |
| Application name | 应用名称，可以自己取 | My Blog Comments |
| Homepage URL | 博客首页地址 | https://your-blog.example.com |
| Application description | 应用说明，可不填 | Gitalk comment system for my blog |
| Authorization callback URL | OAuth 回调地址 | https://your-blog.example.com |

这里最容易出问题的是最后两个地址。

Homepage URL 和 Authorization callback URL 应该根据你实际使用的博客地址填写。如果博客使用的是 HTTPS，就不要写成 HTTP；如果博客使用了自定义域名，也应该填写实际使用的域名。

### 3. 获取 Client ID 和 Client Secret

点击 Register application 后，GitHub 会显示：

- Client ID
- Client Secret

其中 Client ID 可以直接用于 Gitalk 配置，而 Client Secret 属于私密凭证。

如果页面要求生成新的 Secret，需要点击：

```
Generate a new client secret
```

然后把两个值保存下来，后面配置主题时会用到。

需要特别注意的是，Client Secret 不应该公开放到代码仓库里。如果已经泄露，后面可以重新生成。

## 二、在 Hexo 主题中启用 Gitalk

不同 Hexo 主题的配置位置并不完全一样。这里以 Fluid 为例。

### 1. 找到主题配置文件

通常可以在博客目录下找到：

```
blog/themes/fluid/_config.yml
```

如果你使用的 Fluid 版本目录结构有所不同，以自己当前主题实际文件位置为准。

### 2. 开启评论功能

在配置文件中找到 comments 相关配置。例如：

```yaml
# 评论插件 # Comment plugin
post:
  comments:
    enable: true
    # 指定的插件，需要同时设置对应插件的必要参数
    # The specified plugin needs to set the necessary parameters
    # Options: utterances | disqus | gitalk | valine | waline | changyan | livere | remark42 | twikoo | cusdis | giscus | discuss
    type: gitalk
```

这里主要看两个值：

```yaml
enable: true
type: gitalk
```

也就是说，主题需要开启评论功能，同时指定使用 Gitalk。

### 3. 填写 Gitalk 参数

继续在主题配置文件里找到 gitalk 部分。可以按照自己的 GitHub 信息填写：

```yaml
# Gitalk
# 基于 GitHub Issues
# Based on GitHub Issues
# https://github.com/gitalk/gitalk
gitalk:
  clientID: '你的 Client ID'
  clientSecret: '你的 Client Secret'
  repo: '你的 GitHub 仓库名'
  owner: '你的 GitHub 用户名'
  admin: ['你的 GitHub 用户名']
  language: 'zh-CN'
  labels: ['Gitalk', 'Comment']
  perPage: 10
  pagerDirection: 'last'
  distractionFreeMode: false
  createIssueManually: false
```

几个主要参数分别对应：

- `clientID`：GitHub OAuth App 的 Client ID。
- `clientSecret`：GitHub OAuth App 的 Client Secret。
- `repo`：存放评论 Issue 的 GitHub 仓库名称。
- `owner`：GitHub 用户名。
- `admin`：Gitalk 管理员账号，可以填写一个或多个 GitHub 用户名。
- `language`：评论区语言，这里使用中文。
- `labels`：创建 Issue 时使用的标签。
- `perPage`：每页显示多少条评论。
- `pagerDirection`：评论分页的排序方向。
- `distractionFreeMode`：是否使用无干扰模式。
- `createIssueManually`：是否手动创建 Issue。

例如，如果博客仓库地址是：

```
https://github.com/your-username/your-blog-repository
```

那么对应配置应该是：

```yaml
repo: 'your-blog-repository'
owner: 'your-username'
```

这里分别填写仓库名和 GitHub 用户名。

如果博客不是放在 username.github.io 这种仓库里，例如仓库叫 `my-blog`，那么 `repo` 就应该填写：

```yaml
repo: 'my-blog'
```

而不是博客地址。

## 三、重新生成并部署 Hexo

主题配置修改完以后，需要重新生成静态文件并部署。

先清理之前生成的文件：

```bash
hexo clean
```

然后重新生成：

```bash
hexo generate
```

也可以使用简写：

```bash
hexo g
```

最后部署：

```bash
hexo deploy
```

或者：

```bash
hexo d
```

如果希望一次执行完，可以直接：

```bash
hexo clean && hexo g && hexo d
```

部署完成以后，再打开博客文章页面检查评论区。

## 四、第一次使用时初始化评论

Gitalk 第一次加载某篇文章时，如果 GitHub 上还没有对应的 Issue，评论区不会直接出现空白评论框，而是会提示需要初始化。例如可能看到：

```
未找到相关的 Issues 进行评论
请联系 @your-username 初始化创建
```

这里的 `your-username` 只是示意，实际页面会显示 Gitalk 配置中的管理员用户名。

这时候需要使用管理员账号完成初始化。

### 1. 使用 GitHub 登录

点击「使用 GitHub 登录」，然后按照 GitHub 页面提示授权刚刚创建的 OAuth App。

### 2. 创建对应 Issue

登录成功后，如果当前用户属于 Gitalk 配置中的 admin，就可以进行评论初始化。点击初始化评论后，Gitalk 会在配置的仓库中创建对应的 Issue。

之后，这个 Issue 就作为当前文章的评论存储位置。

### 3. 检查评论区

如果初始化成功，评论区应该会变成类似「暂无评论」，这时就可以发表评论了。

## 五、最终效果

Gitalk 正常工作后，文章底部会出现评论区域。大致可以理解成下面这个结构：

````
┌─────────────────────────────────────────┐
│ 使用 GitHub 登录                          │
├─────────────────────────────────────────┤
│ [头像] 用户名                             │
│ 这是一条测试评论，支持 **Markdown** 语法   │
│                                          │
│ ```python                                │
│ print("Hello, Gitalk!")                  │
│ ```                                      │
│                                          │
│ 2 小时前                                  │
└─────────────────────────────────────────┘
````

实际页面样式会根据 Gitalk 和博客主题的版本有所区别。

## 六、常见问题

配置 Gitalk 的时候，真正麻烦的地方往往不是安装，而是某个参数看起来没问题，评论区却还是不能用。下面把几个比较常见的情况列出来。

### 1. 评论区显示 Error: Not Found

一般先检查仓库和用户名。重点看：

```yaml
repo: '你的仓库名'
owner: '你的 GitHub 用户名'
```

确认：

- repo 是真实存在的仓库名称；
- owner 是对应的 GitHub 用户名；
- 仓库名称没有写错；
- 大小写与实际仓库保持一致。

### 2. 显示 Error: Validation Failed

一种常见原因是 Issue 标题不符合 GitHub 的限制。

Gitalk 通常会使用文章标题等信息来定位对应 Issue。如果文章标题过长，就可能触发 GitHub 的校验错误。

可以先尝试：

- 缩短文章标题；
- 或根据实际使用的 Gitalk / 主题版本配置 `id`，让文章路径参与 Issue 的唯一标识。

例如可以使用文章路径，而不是完全依赖标题。

### 3. 点击登录后无法返回博客

这种情况优先检查 GitHub OAuth App 的回调地址。回到：

```
GitHub → Settings → Developer settings → OAuth Apps
```

找到刚才创建的 OAuth App，检查 Authorization callback URL 是否和实际博客地址一致。

尤其注意 `http://` 和 `https://` 并不是同一个地址。如果博客使用自定义域名，也不要继续填写旧的 GitHub Pages 地址。

### 4. 评论区完全不显示

先检查主题配置：

```yaml
post:
  comments:
    enable: true
    type: gitalk
```

确认：

```yaml
enable: true
```

并且：

```yaml
type: gitalk
```

已经设置正确。

如果这些配置都没问题，还要继续检查文章本身有没有关闭评论。

## 七、一个容易忽略的问题：文章自己的 comments 配置

如果前面的 OAuth、Gitalk 参数和主题配置都检查过了，但评论区还是没有出现，可以看看文章的 Front-matter。

Hexo 文章通常会有这样的文件头：

```yaml
---
title: 我的第一篇文章
date: 2025-11-16 10:00:00
tags: [Hexo, Blog]
---
```

如果当前主题的逻辑要求文章显式开启评论，可以加上：

```yaml
---
title: 我的第一篇文章
date: 2025-11-16 10:00:00
tags: [Hexo, Blog]
comments: true
---
```

这里的 `comments: true` 就是告诉主题，这篇文章需要显示评论区。

### 排查这个问题时，建议按顺序检查

以本文遇到的情况为例，前面的配置都正常：

- GitHub OAuth App 的 Client ID 和 Client Secret 没有填错；
- Authorization callback URL 和博客线上地址一致；
- Fluid 的 `_config.yml` 中 `post.comments.enable: true`；
- 评论类型已经设置成 `type: gitalk`；
- Gitalk 的 repo、owner、admin 等参数也都正确。

但评论区仍然没有加载。

继续检查主题代码之后，发现文章本身还需要设置：

```yaml
comments: true
```

加上之后，评论区就正常出现了。

所以，如果你已经确认 Gitalk 本身没有配置错误，别忘了检查文章 Front-matter。

## 八、不想给每篇文章都加 comments: true 怎么办？

如果博客文章比较多，一篇篇修改 Front-matter 会比较麻烦。这种情况下，可以直接调整 Fluid 的评论模板，让开启主题评论后，文章默认显示评论区。

### 1. 找到评论模板

例如：

```
blog/themes/fluid/layout/_partials/comments.ejs
```

打开后，找到类似下面的判断：

```ejs
<% if ((!is_post() && !is_page()) || (is_post() && theme.post.comments.enable && page.comments) || (is_page() && page.comments)) { %>
```

这里的 `&& page.comments` 就是文章必须显式设置 comments 的原因。

### 2. 修改判断条件

把：

```ejs
<% if ((!is_post() && !is_page()) || (is_post() && theme.post.comments.enable && page.comments) || (is_page() && page.comments)) { %>
```

修改成：

```ejs
<% if ((!is_post() && !is_page()) || (is_post() && theme.post.comments.enable) || (is_page() && page.comments)) { %>
```

这样以后，文章页面只要主题层面的 `theme.post.comments.enable` 开启，就会显示评论区。

### 3. 重新部署

修改完成后重新生成并部署：

```bash
hexo clean && hexo g && hexo d
```

这样就不用给每一篇文章单独写 `comments: true` 了。

### 这个修改具体改变了什么？

修改前：

```
is_post() && theme.post.comments.enable && page.comments
```

需要同时满足：

- 当前是文章页；
- 主题的评论功能已经打开；
- 当前文章设置了 comments。

修改后：

```
is_post() && theme.post.comments.enable
```

文章页只需要主题评论功能开启即可。这样 `comments: true` 就不再是必填项。

如果某篇文章不希望显示评论，则需要显式设置 `comments: false`。

另外，这个修改只针对文章页。页面（page）的评论判断仍然保留原来的逻辑。

还有一点需要留意：如果以后升级 Fluid 主题，主题文件可能被更新覆盖。改过模板的话，最好自己保留一份修改记录，或者直接使用 Git 管理主题文件。

### 这里其实还有一个排查思路

遇到这种「所有配置看起来都对，但功能就是不出现」的问题，不要一直重复检查 Client ID、仓库名这些参数。

如果确认 Gitalk 本身已经加载，可以直接去看主题对应的模板文件。例如：

```
layout/_partials/comments.ejs
```

看看主题到底在什么条件下渲染评论组件。这种方法对 Hexo 主题里的很多问题都适用。配置文件负责告诉主题「用什么」，模板代码则决定「什么时候显示」。

## 九、几个可以顺手调整的地方

Gitalk 能正常使用之后，还可以根据自己的博客习惯做一些简单调整。

### 1. 修改评论区样式

如果觉得默认样式和博客不太协调，可以通过自定义 CSS 调整。例如：

```css
/* 自定义 Gitalk 样式 */
.gt-container {
  font-family: 'Microsoft YaHei', sans-serif;
}
.gt-header-textarea {
  border-radius: 8px;
}
.gt-btn-public {
  background-color: #0084ff;
}
```

具体样式选择器还是以当前 Gitalk 版本的实际页面结构为准。

如果只是修改字体、输入框圆角、按钮样式，一般不需要动 Gitalk 本身的 JavaScript 配置。

### 2. 接收评论通知

Gitalk 的评论最终对应 GitHub Issue，因此评论更新可以通过 GitHub 的通知机制来处理。可以在 GitHub 中调整邮件通知：

```
GitHub 头像 → Settings → Notifications → Email notification preferences
```

根据自己的需求选择通知方式。

### 3. 文章很多时怎么初始化？

如果已经有很多旧文章，每篇文章第一次使用 Gitalk 时都需要对应的 Issue。这种情况下，可以按文章逐个访问并完成初始化。

如果文章数量很多，也可以进一步写脚本，通过文章列表批量处理对应的 Issue。不过如果博客文章数量并不多，手动初始化通常更简单，也更容易确认每篇文章是否正常。

## 十、Gitalk 和其他评论系统怎么选？

如果你还没有决定使用哪种评论系统，可以简单看一下几个常见方案：

| 特性 | Gitalk | Disqus | Valine | Utterances |
| --- | --- | --- | --- | --- |
| 免费 | ✅ | ❌（有广告） | ✅ | ✅ |
| 无需后端 | ✅ | ✅ | ❌ | ✅ |
| Markdown 支持 | ✅ | ❌ | ✅ | ✅ |
| 数据自主 | ✅ | ❌ | ❌ | ✅ |
| 登录方式 | GitHub | 多种 | 匿名 | GitHub |
| 适用场景 | 技术博客 | 通用博客 | 个人博客 | 技术博客 |

如果博客本身就在 GitHub Pages 上，并且读者主要是开发者，Gitalk 和 Utterances 都比较自然。Gitalk 使用 GitHub Issues 保存评论，管理起来也比较直观。对于已经习惯 GitHub 工作流的人来说，评论和代码仓库可以放在同一个平台上管理。

## 总结

整个配置过程其实可以压缩成四步：

1. **创建 GitHub OAuth App**：拿到 Client ID 和 Client Secret，并正确填写博客首页和 OAuth 回调地址。

2. **在 Fluid 中开启 Gitalk**：在主题配置里设置：

   ```yaml
   post:
     comments:
       enable: true
       type: gitalk
   ```

   然后填写：

   ```yaml
   gitalk:
     clientID: '你的 Client ID'
     clientSecret: '你的 Client Secret'
     repo: '你的仓库名'
     owner: '你的 GitHub 用户名'
     admin: ['你的 GitHub 用户名']
   ```

3. **重新生成并部署**：

   ```bash
   hexo clean && hexo g && hexo d
   ```

4. **第一次访问文章时初始化 Issue**：使用 GitHub 登录，并由管理员创建当前文章对应的 Issue。

如果评论区仍然没有出现，再检查文章 Front-matter 是否有 `comments: true`，或者根据自己的需求修改 Fluid 的评论模板，让文章默认开启评论。

## 延伸阅读

- [Gitalk 官方文档](https://github.com/gitalk/gitalk)
- [GitHub OAuth Apps 文档](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [Hexo 官方文档](https://hexo.io/zh-cn/docs/)
- [Fluid 主题文档](https://hexo.fluid-dev.com/docs/)