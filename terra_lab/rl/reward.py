from enum import Enum


class Reward(Enum):
    WIN = 1000
    LOSE = -1000
    WRONG_INPUT = -100
    NOT_ENOUGHT_MONEY = -100
    MOVE = -1
