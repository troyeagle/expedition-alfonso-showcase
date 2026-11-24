# HTML 自动发布规约

## 发布位置与边界

- 本地目录是 `flight-price-watch/expedition-alfonso-showcase`，Git 远端是独立仓库 [`troyeagle/expedition-alfonso-showcase`](https://github.com/troyeagle/expedition-alfonso-showcase)。读取 PAT 应授权这个仓库。
- 源码发布分支：`main`；线上入口：[空间对齐辅助工具](https://troyeagle.github.io/expedition-alfonso-showcase/)。
- 编辑 `assets/embedded-scene.html` 中的场景，用原有 `build-page.py` 将最新场景嵌入 `assets/public-source.html`。
- `scripts/build_static_pages.py` 重建并验证包装页面和场景一致，只导出 `dist/index.html` 与 `dist/LICENSE.txt`。原始来源快照、验证截图、报告及测试脚本不进入产物。
- 保留软件 MIT 许可和第三方代码声明；剧本版权及原始演示鸣谢见 [README](../README.md)。

## 本地检查

在本工程根目录运行，Python 标准库即可：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_static_pages.py
python3 -m http.server 8769 --directory dist
```

打开 <http://localhost:8769/>，检查场景、门状态、进度控制及房间对应关系。直接修改打包页面中嵌入的场景会在下次重建时覆盖；场景源码是 `assets/embedded-scene.html`，包装层需修改 `assets/public-source.html`。

## 发布流程

1. 将场景、包装层、构建器、测试或文档变化提交并推送 `main`。`dist/` 是生成目录，不提交到源码仓库。
2. [源码工作流](https://github.com/troyeagle/expedition-alfonso-showcase/actions/workflows/publish-static.yml) 对 push、PR 与手动运行执行验证和构建；仅 `main` 的 push 或手动运行上传 `site-expedition-alfonso-showcase`。PR 不生成正式产物或通知博客。
3. 调用的共享工作流和 `publisher_ref` 固定到同一完整提交 SHA；升级时一起更新两处，通过测试后再发布。公共流程使用 Python 3.12、Node 22 和静态文件打包器，无需安装本工程第三方依赖。
4. `_site-sync.json` 包含源码版本、运行身份及逐文件哈希。博客验证来源、源历史、路径、内容和所有 HTML 的本地资源引用，然后仅更新 `/expedition-alfonso-showcase/` 与发布状态；正常产物更新直接提交博客 `master`，再由 Pages 部署。

## 配置与运行入口

- [本仓库 Actions Secrets](https://github.com/troyeagle/expedition-alfonso-showcase/settings/secrets/actions)：可选保存 `BLOG_DISPATCH_TOKEN`，仅授权 **博客仓库 Actions: write**。成功构建会立即请求同步。可以复用其他源码仓库的通知 PAT，但每个个人仓库需单独保存 Secret。
- 没有通知 Secret 时，博客仍约每 30 分钟自动收集，GitHub 调度可能延迟。要立即手动同步，在 [博客工作流](https://github.com/troyeagle/troyeagle.github.io/actions/workflows/sync-apps.yml) 选择 `master`、取消 `dry_run`，不勾选 `include_disabled`。
- [博客白名单](https://github.com/troyeagle/troyeagle.github.io/blob/master/.github/apps.json)：`expedition-alfonso-showcase.enabled` 控制本项目启停。
- [博客变量](https://github.com/troyeagle/troyeagle.github.io/settings/variables/actions)：两个全局开关 `SITE_SYNC_ENABLED`、`SITE_SYNC_PUBLISH_ENABLED` 均为 `true` 才会正式同步。
- [博客 Secrets](https://github.com/troyeagle/troyeagle.github.io/settings/secrets/actions)：`SOURCE_ARTIFACTS_TOKEN` 对本仓库只需 Contents: read、Actions: read；`BLOG_PUBLISH_TOKEN` 只授权博客 Contents: write，并只保存在博客。
- [已发布版本](https://github.com/troyeagle/troyeagle.github.io/blob/master/.github/apps-state.json)：核对 `sha`、`runId` 和 `runNumber`。

## 接入、暂停与恢复

首次接入保持白名单 `enabled: false`；源码成功构建后，在博客勾选 `dry_run` 与 `include_disabled` 预览，再启用并真实同步。日常发布无需重复接入步骤。

回退前先暂停此项目，优先在源码以新提交恢复内容并重建，避免定时同步覆盖回退。不要重写源码历史；14 天后过期的产物可通过源码 `main` 手动重建。通知 Token 和读取 Token 各按自己的权限续期，值只保存在 Secrets 中。
