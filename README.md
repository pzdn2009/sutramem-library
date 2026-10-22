# 在线经藏

这是公开的 SutraMem 内容仓库，并以 Git submodule 的方式嵌入私有 iOS App 仓库。App 读取：

`https://raw.githubusercontent.com/pzdn2009/sutramem-library/main/catalog.json`

新增或修改经典时，在这个仓库提交内容；随后在 App 仓库更新 submodule 指针。

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
