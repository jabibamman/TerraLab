from enum import Enum

from terra_lab.utils.machine import Machine
from terra_lab.utils.state import State


class MAP_STATES(Enum):
    UNFERTILE_DIRT = State(value=0, color=(115, 82, 64))
    ROCK = State(value=1, color=(105, 105, 105))
    WIND_TURBINE = State(value=2, color=(100, 100, 100))
    PURIFIER = State(value=3, color=(181, 0, 0))
    FERTILE_DIRT = State(value=4, color=(133, 51, 8))
    IRRIGATOR = State(value=5, color=(4, 79, 18))
    GRASS = State(value=6, color=(0, 235, 12))


class MACHINE_TYPE(Enum):
    WIND_TURBINE = Machine(name="WIND_TURBINE", range=6, price=50)
    PURIFIER = Machine(name="PURIFIER", range=5, price=25)
    IRRIGATOR = Machine(name="IRRIGATOR", range=7, price=25)
