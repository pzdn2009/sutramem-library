# 在线经藏

这个目录和 iOS App 放在同一个仓库中。App 发布后读取：

`https://pzdn2009.github.io/foshi-counter-ios/catalog.json`

仓库可以保持私有；发布时只把 `OnlineLibrary` 目录推送到同一仓库的 `gh-pages` 分支。

## 当前范围

- `catalog.json` 是在线书目入口。
- 第一版只展示经典、版本、支持的学习模式和章节目录。
- 正文下载、本地安装和版本更新在下一步接入。

## 新增一本经典

在 `catalog.json` 的 `books` 数组中增加一项。`id` 一经发布应保持稳定；章节 `id` 也应保持稳定，以便未来保存阅读、背诵与念诵进度。

状态约定：

- `preview`：只开放目录预览。
- `available`：正文包已经准备好，可以下载。

发布内容前需要核对文本来源和使用许可。
