"""仿真核心的单元测试。运行：cd backend && pytest tests -q"""

import sys
from pathlib import Path

# 无论从项目根目录还是 backend 目录运行测试，都能 import 到仿真模块。
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from map_data import MAP_HEIGHT, MAP_WIDTH
from simulation import RobotSimulation


def test_initial_state():
    state = RobotSimulation().snapshot()
    assert state == {"x": 1, "y": 1, "direction": "E", "status": "idle"}


def test_forward_moves_east():
    state = RobotSimulation().move("forward")
    assert (state["x"], state["y"]) == (2, 1)
    assert state["direction"] == "E"
    assert state["status"] == "moving"


def test_turn_right_changes_direction_without_moving():
    state = RobotSimulation().move("right")
    assert state["direction"] == "S"
    assert (state["x"], state["y"]) == (1, 1)


def test_turn_left_changes_direction_without_moving():
    state = RobotSimulation().move("left")
    assert state["direction"] == "N"
    assert (state["x"], state["y"]) == (1, 1)


def test_four_right_turns_return_to_start_direction():
    robot = RobotSimulation()
    directions = [robot.move("right")["direction"] for _ in range(4)]
    assert directions == ["S", "W", "N", "E"]


def test_boundary_blocks_movement_and_keeps_position():
    robot = RobotSimulation()
    # 19 是东边界最后一格；y=1 这一行没有障碍物。
    for _ in range(MAP_WIDTH - 2):
        robot.move("forward")
    before = robot.snapshot()
    after = robot.move("forward")
    assert (after["x"], after["y"]) == (before["x"], before["y"])
    assert after["x"] == MAP_WIDTH - 1
    assert after["status"] == "blocked"


def test_obstacle_blocks_movement():
    robot = RobotSimulation()
    for _ in range(4):  # (1,1) -> (5,1)
        robot.move("forward")
    robot.move("right")  # 朝南
    robot.move("forward")  # (5,2)
    blocked = robot.move("forward")  # (5,3) 是障碍物
    assert (blocked["x"], blocked["y"]) == (5, 2)
    assert blocked["status"] == "blocked"


def test_reset_restores_initial_state():
    robot = RobotSimulation()
    robot.move("forward")
    state = robot.move("reset")
    assert state == {"x": 1, "y": 1, "direction": "E", "status": "idle"}


def test_invalid_command_raises():
    with pytest.raises(ValueError):
        RobotSimulation().move("jump")


def test_robot_always_inside_map():
    robot = RobotSimulation()
    for command in ("forward", "right", "forward", "left", "forward"):
        state = robot.move(command)
        assert 0 <= state["x"] < MAP_WIDTH
        assert 0 <= state["y"] < MAP_HEIGHT
