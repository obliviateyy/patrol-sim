# 基于 Web 的智能巡检机器人二维仿真系统

> **在线演示：** 部署后把实际访问地址写在这里，访客打开即可体验。（当前项目骨架已完成，尚未部署演示站点。）

把巡检机器人的场景搬进浏览器：打开页面就能看到一张二维地图，用按钮手动控制机器人前进和转向，并实时看到它的位置、朝向和运行状态如何变化。

## 这个项目能做什么

- **查看二维地图**：网格地图中标出地图边界、障碍物和可通行区域，机器人用带朝向标识的圆点表示。
- **手动控制机器人**：点击「前进」「左转」「右转」发出指令，机器人按指令移动。
- **状态反馈**：页面显示横坐标、纵坐标、朝向和运行状态，数据直接来自后端 API，每 2 秒自动同步。
- **安全边界**：机器人尝试越出地图边界或撞上障碍物时，会停在原地并显示「受阻」状态。
- **可验证、可部署**：后端核心有单元测试，提交后由 GitHub Actions 自动运行；提供 Docker 部署方式，一条命令即可启动。

## 快速开始

```bash
# 安装依赖
python -m pip install -r backend/requirements.txt

# 启动服务（同时提供页面和 API）
cd backend
set SERVE_FRONTEND=1 && python app.py
```

打开 <http://localhost:5000> 即可操作。Windows PowerShell 用户请用 `$env:SERVE_FRONTEND=1; python app.py`。

也可以用 Docker：

```bash
docker compose up --build
# 打开 http://localhost:8000
```

详细步骤见[运行与结业提交](docs/04_运行与结业提交.md)。

## 技术选型

- 前端：原生 HTML / CSS / JavaScript，Canvas 绘制地图
- 后端：Python 3.11 + Flask，提供地图、状态和手动控制 API
- 仿真：纯 Python 状态机，位置、朝向、边界与障碍判定
- 测试：pytest；CI：GitHub Actions
- 部署：Docker 单镜像 + Docker Compose，由 Flask 同时提供页面和 API

## 项目文档

- [项目需求](docs/01_项目需求.md)：功能范围和验收方式
- [小组分工](docs/02_小组分工.md)：成员及各自完成的内容
- [项目架构与接口](docs/03_项目架构与接口.md)：模块职责、数据流向和接口约定
- [运行与结业提交](docs/04_运行与结业提交.md)：本地启动、Docker 部署与结业材料
