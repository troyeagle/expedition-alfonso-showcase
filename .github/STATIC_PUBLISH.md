# 独立 GitHub Pages 发布规约

## 站点归属与地址

- 本工程是公开仓库 [`troyeagle/expedition-alfonso-showcase`](https://github.com/troyeagle/expedition-alfonso-showcase)，拥有自己的项目 Pages。
- 线上入口：[空间对齐辅助工具](https://troyeagle.github.io/expedition-alfonso-showcase/)。地址由账号和仓库名决定；本地位于 `flight-price-watch/` 下不影响站点归属。
- 源码分支是 `main`。本仓库独立构建和部署，使用 GitHub 自动提供的 `GITHUB_TOKEN` 和 OIDC；不需要 PAT、博客通知 Secret 或跨仓库复制。

## 源码和发布边界

编辑 `assets/embedded-scene.html` 中的场景，用 `build-page.py` 将场景嵌入 `assets/public-source.html`。包装层修改在 `assets/public-source.html` 中维护；直接编辑其中嵌入的场景，会在重建时覆盖。

`scripts/build_static_pages.py` 调用原有打包器并验证场景一致性，只导出 `dist/index.html` 和 `dist/LICENSE.txt`。`dist/` 是生成目录，不提交到源码仓库。原始来源快照、验证截图、报告和测试脚本不进入站点；软件与第三方代码的许可证声明须保留，剧本版权和鸣谢见 [README](../README.md)。

## 本地检查

在工程根目录运行，Python 标准库即可：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_static_pages.py
python3 -m http.server 8769 --directory dist
```

打开 <http://localhost:8769/>，检查场景、门状态、进度控制和房间对应关系。页面资源使用相对路径或内嵌数据，可以直接打开，也适用于项目站的 `/expedition-alfonso-showcase/` 子路径。

## 自动构建与部署

[发布工作流](https://github.com/troyeagle/expedition-alfonso-showcase/actions/workflows/publish-static.yml) 位于本仓库 `.github/workflows/publish-static.yml`，自包含地运行官方 Pages 动作，固定动作版本到完整提交 SHA。

1. `main` 的 push 和手动运行执行四项页面检查、重建，并通过 `actions/upload-pages-artifact` 上传 `dist/`，产物名为 `github-pages`，保留 1 天。
2. 独立部署任务调用 `actions/deploy-pages`，使用 `github-pages` 环境，将该产物发布为本仓库的项目站。
3. PR 只验证和构建，不上传正式 Pages 产物，也不部署。
4. 构建任务只有 Contents: read、Pages: read；部署任务只有 Pages: write、ID-token: write。同一分支的发布按顺序执行，发布中的任务不会被新提交取消。

无需等待博客的半小时收集，也不再生成 `site-expedition-alfonso-showcase`、`_site-sync.json` 或博客发布状态记录。历史运行和提交保留作审计记录。

## GitHub 配置入口

- [Pages 设置](https://github.com/troyeagle/expedition-alfonso-showcase/settings/pages)：Build and deployment → Source 选择 **GitHub Actions**。
- [工作流运行](https://github.com/troyeagle/expedition-alfonso-showcase/actions/workflows/publish-static.yml)：查看检查和部署结果；需要手动重建时选择 `main` 后运行。
- [部署环境](https://github.com/troyeagle/expedition-alfonso-showcase/settings/environments)：`github-pages` 环境用于项目站部署。如设置分支保护，应允许 `main` 部署。
- [分支规则](https://github.com/troyeagle/expedition-alfonso-showcase/settings/branches)：如需人工审核，在源码合入 `main` 前设置 PR 和检查要求。

本站使用默认项目地址，未设置独立域名。构建器、工作流、检查和发布规约均与源码一起提交到 `main`。

## 暂停与恢复

暂停自动发布可在源码工作流菜单中选择 Disable workflow；恢复后 Enable workflow 并在 `main` 手动运行。恢复旧内容优先使用新提交或 `git revert`，推送后由本仓库重新部署；不重写分支历史。

如需下线站点，可在本仓库 Pages 设置中操作。迁移后，博客仓库没有此目录的副本、收集配置或写入权限白名单，不参与本项目恢复。
