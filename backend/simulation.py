"""巡检机器人仿真核心：位置、朝向、运行状态和移动判定。

本模块不依赖 Web 框架，打开终端就能单独测试，便于 CI 跑单元测试。
"""

from map_data import (
    START_DIRECTION,
    START_X,
    START_Y,
    is_blocked,
    is_inside,
)

DIRECTIONS = ("N", "E", "S", "W")  # 北 东 南 西

# y 轴向下为正，所以向北是 y - 1。
_DELTAS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

_LEFT = {"N": "W", "W": "S", "S": "E", "E": "N"}
_RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}

VALID_COMMANDS = ("forward", "left", "right", "reset")
VALID_STATUSES = ("idle", "moving", "blocked")


class RobotSimulation:
    """单机器人仿真状态机。"""

    def __init__(self):
        self.reset()

    def reset(self):
        """回到起点，朝向起点方向，状态置为 idle。"""
        self.x = START_X
        self.y = START_Y
        self.direction = START_DIRECTION
        self.status = "idle"
        return self.snapshot()

    def snapshot(self):
        """返回当前状态副本，避免调用方直接改内部字段。"""
        return {
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "status": self.status,
        }

    def move(self, command):
        """执行一条指令，返回执行后的最新状态。

        指令：forward 前进一格、left 左转、right 右转、reset 重置。
        前进时若目标越界或撞上障碍物，位置不变，状态置为 blocked。
        """
        if command == "reset":
            return self.reset()

        if command == "left":
            self.direction = _LEFT[self.direction]
            self.status = "idle"
            return self.snapshot()

        if command == "right":
            self.direction = _RIGHT[self.direction]
            self.status = "idle"
            return self.snapshot()

        if command == "forward":
            dx, dy = _DELTAS[self.direction]
            next_x, next_y = self.x + dx, self.y + dy
            if not is_inside(next_x, next_y) or is_blocked(next_x, next_y):
                self.status = "blocked"
            else:
                self.x, self.y = next_x, next_y
                self.status = "moving"
            return self.snapshot()

        raise ValueError(f"未知指令: {command}")
