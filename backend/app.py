"""后端 API 入口。

本地开发：cd backend && python app.py
Docker 部署：设置 SERVE_FRONTEND=1，由本服务同时提供页面和 API。
"""

import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

import map_data
from simulation import VALID_COMMANDS, RobotSimulation

app = Flask(__name__)
simulator = RobotSimulation()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
SERVE_FRONTEND = os.environ.get("SERVE_FRONTEND", "0") == "1"


@app.after_request
def add_cors_headers(response):
    """本地开发时前端在另一端口，需要允许跨域读取响应。"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.get("/api/health")
def health():
    """健康检查，供 Render 等平台探测服务是否就绪。"""
    return jsonify({"status": "ok"})


@app.get("/api/map")
def get_map():
    """返回地图尺寸和障碍物坐标。"""
    return jsonify(map_data.to_dict())


@app.get("/api/robot")
def get_robot():
    """返回机器人最新状态。"""
    return jsonify(simulator.snapshot())


@app.post("/api/robot/move")
def move_robot():
    """执行手动控制指令，返回执行后的最新状态。"""
    payload = request.get_json(silent=True) or {}
    command = payload.get("command")
    if command not in VALID_COMMANDS:
        return jsonify({"error": f"无效指令，应为 {', '.join(VALID_COMMANDS)}"}), 400
    return jsonify(simulator.move(command))


if SERVE_FRONTEND:
    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:filename>")
    def frontend_files(filename):
        if filename.startswith("api/"):
            return jsonify({"error": "接口不存在"}), 404
        return send_from_directory(FRONTEND_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
