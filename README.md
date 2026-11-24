# 《远征队失联事件》辅助工具

`expedition-alfonso-showcase` 是剧本杀《远征队失联事件》的空间对齐辅助工具，用于观察现实世界与锚定世界在不同门状态下的旋转过程，以及对齐后的房间对应关系。

## 版权与许可

- **剧本版权**：《远征队失联事件》的版权归原作者所有。本项目的软件许可证不授予对剧本正文、角色、剧情、设定及其他受保护内容的使用权。
- **灵感与鸣谢**：本项目灵感来自乐观的大鹏鸟制作的“16种门状态互动演示”。感谢其提供的演示和思路，并允许本项目发布。
- **软件许可**：本软件遵循 [MIT 协议](LICENSE)，允许在遵守许可证的前提下使用、修改和分发。
- **第三方代码**：项目保留了 Floating UI 等第三方代码原有的版权与许可证声明。

软件的 MIT 授权与剧本的版权分别适用。使用和分发本工具时，请尊重剧本原作者的权利，并保留软件及第三方代码所需的版权声明和许可证文本。

## 鸣谢与来源

- 乐观的大鹏鸟：[B 站主页](https://space.bilibili.com/434669937)。
- [原始“16种门状态互动演示”](https://door-worlds-sixteen-leguandedapengniao-d7cep410ff9d1.webapps.tcloudbase.com/)。

本项目在原始演示基础上增加了双世界房号、房间重合对应、体积比例及走廊配色等功能。

## 功能

- 选择 16 种门状态组合，播放或手动控制旋转对齐过程。
- 旋转视角、缩放场景，观察三层建筑的空间关系。
- 显示全部房号、只显示自选房间，或聚焦一个房间及其对应房间。
- 查看对齐后的实际房间重合、走廊和建筑外所占比例。
- 用不同颜色区分两个世界、各自的走廊和选中房间的实际重合区域。

## 使用

直接用浏览器打开 `assets/public-source.html` 即可使用，也可以通过本地服务器预览。在本目录运行：

```bash
python3 -m http.server 8767 --directory assets
```

然后打开 <http://localhost:8767/public-source.html>。

线上访问：[空间对齐辅助工具](https://troyeagle.github.io/expedition-alfonso-showcase/)。本公开仓库独立发布项目 GitHub Pages，推送 `main` 后自动检查、构建并部署；本地验证、Pages 设置及私有化回退步骤见 [发布规约](.github/STATIC_PUBLISH.md)。

## 修改与打包

场景源码位于 `assets/embedded-scene.html`。修改后，在本目录运行：

```bash
python3 build-page.py
```

脚本会将最新场景嵌入 `assets/public-source.html`，生成可直接打开的单文件页面。直接修改打包页面中的场景代码，会在下次打包时被覆盖。

`assets/original-public-source.html` 和 `assets/original-embedded-scene.html` 保留原始演示快照，便于核对来源与修改。
