"""地图定义。

坐标约定：原点在左上角，x 向右递增，y 向下递增，一个格子为一个单位。
完整约定见 docs/03_项目架构与接口.md。
"""

MAP_WIDTH = 20
MAP_HEIGHT = 15

# 障碍物坐标 (x, y)。前端按这份数据绘制深色格子。
OBSTACLES = frozenset({
    (5, 3), (5, 4), (5, 5),
    (10, 8), (11, 8), (12, 8),
    (14, 2), (14, 3),
})

START_X = 1
START_Y = 1
START_DIRECTION = "E"


def is_inside(x, y):
    """坐标是否落在地图内。"""
    return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT


def is_blocked(x, y):
    """坐标是否为障碍物。"""
    return (x, y) in OBSTACLES


def to_dict():
    """给 API 用的地图数据。"""
    return {
        "width": MAP_WIDTH,
        "height": MAP_HEIGHT,
        "obstacles": [[x, y] for x, y in sorted(OBSTACLES)],
    }
