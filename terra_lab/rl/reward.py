from enum import Enum

from terra_lab.utils.enums import MACHINE_TYPE


class Reward(Enum):
    WIN = 50000
    LOSE = -1000
    WRONG_INPUT = -1000
    NOT_ENOUGHT_MONEY = -100
    MOVE = -5
    PLACE_WIND_TURBINE = (MACHINE_TYPE.WIND_TURBINE.value.range * 2 + 1) ** 2
