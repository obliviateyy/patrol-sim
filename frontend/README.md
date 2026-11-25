# 前端说明

原生 HTML / CSS / JavaScript 实现，无构建步骤，无第三方依赖。

## 文件

| 文件 | 作用 |
| --- | --- |
| `index.html` | 页面结构：地图区、控制区、状态面板 |
| `style.css` | 布局与配色 |
| `app.js` | 请求后端 API、Canvas 绘制、控制按钮和状态同步 |

## 运行

项目骨架默认由 Flask 同时托管页面和 API，见[运行与结业提交](../docs/04_运行与结业提交.md)。打开 `http://localhost:5000` 即可。

若要把前端单独起在另一个端口：

1. 把 `app.js` 顶部的 `API_BASE` 从 `""` 改为 `"http://localhost:5000"`。
2. 后端按默认方式启动（不设置 `SERVE_FRONTEND`）。
3. 在本目录起任意静态服务器，例如 `python -m http.server 8080`，再打开 `http://localhost:8080`。

后端已开启跨域响应头，单独起前端时可直接请求 API。

## 页面行为

- 打开时并行请求 `GET /api/map` 和 `GET /api/robot`，按 20×15 网格绘制地图、障碍物和带朝向箭头的机器人。
- 点击「前进」「左转」「右转」向 `POST /api/robot/move` 发送对应 `command`，用响应更新状态并重绘。
- 点击「重置」回到起点。
- 每 2 秒轮询 `GET /api/robot`，保证页面显示与 API 返回一致。
- 遇到越界或障碍物时，页面提示「前方越界或遇到障碍物，机器人已停在原地。」，机器人显示为深红色。
