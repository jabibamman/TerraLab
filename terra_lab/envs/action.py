from enum import Enum

from terra_lab.envs.position import Position


class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    PLACE_WIND_TURBINE = 5
    PLACE_IRRIGATOR = 6
    PLACE_PURIFIER = 7

MOVES = {
    Action.UP : Position(0, -1),
    Action.DOWN : Position(0, 1),
    Action.LEFT : Position(1, 0),
    Action.RIGHT : Position(-1, 0)
}