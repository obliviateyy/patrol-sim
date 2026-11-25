# 后端说明

基于 Flask 的仿真 API。核心逻辑在 `simulation.py`，不依赖 Web 框架，可直接用 pytest 测试。

## 启动

```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```

默认只开启 API（端口 5000）。设置 `SERVE_FRONTEND=1` 后，同一进程还会托管 `frontend/` 目录的页面：

```bash
# Windows CMD
set SERVE_FRONTEND=1 && python app.py
# Windows PowerShell
$env:SERVE_FRONTEND=1; python app.py
# Linux / Git Bash
SERVE_FRONTEND=1 python app.py
```

## 接口与请求示例

以下命令在 Git Bash 或 Linux 终端执行，服务需已启动。

获取地图：

```bash
curl http://localhost:5000/api/map
# {"height":15,"obstacles":[[5,3],[5,4],[5,5],[10,8],[11,8],[12,8],[14,2],[14,3]],"width":20}
```

获取机器人状态：

```bash
curl http://localhost:5000/api/robot
# {"direction":"E","status":"idle","x":1,"y":1}
```

发送前进指令：

```bash
curl -X POST http://localhost:5000/api/robot/move \
  -H "Content-Type: application/json" \
  -d '{"command":"forward"}'
# {"direction":"E","status":"moving","x":2,"y":1}
```

左转 / 右转 / 重置：

```bash
curl -X POST http://localhost:5000/api/robot/move -H "Content-Type: application/json" -d '{"command":"left"}'
curl -X POST http://localhost:5000/api/robot/move -H "Content-Type: application/json" -d '{"command":"right"}'
curl -X POST http://localhost:5000/api/robot/move -H "Content-Type: application/json" -d '{"command":"reset"}'
```

无效指令返回 HTTP 400：

```bash
curl -i -X POST http://localhost:5000/api/robot/move \
  -H "Content-Type: application/json" -d '{"command":"jump"}'
# HTTP/1.1 400 BAD REQUEST
# {"error":"无效指令，应为 forward, left, right, reset"}
```

机器人连续前进到东边界 `(19, 1)` 后再前进，返回坐标不变且 `status` 为 `blocked`。

## 测试

```bash
cd backend
python -m pytest tests -q
# 10 passed
```
