class Radar:
    def __init__(self, up: bool, down: bool, left: bool, right: bool):
        self.UP = up
        self.DOWN = down
        self.LEFT = left
        self.RIGHT = right

    def __eq__(self, other):
        return self.UP == other.UP and self.DOWN == other.DOWN and self.LEFT == other.LEFT and self.RIGHT == other.RIGHT

    def to_value(self):
        value = 0
        if self.UP:
            value += 1
        if self.DOWN:
            value += 2
        if self.LEFT:
            value += 4
        if self.RIGHT:
            value += 8
        return value


class State:
    def __init__(self, next_stone: Radar, next_wind_turbine: Radar, distance_next_wind_turbine: int, bloc_type: int):
        self.next_stone = next_stone
        self.next_wind_turbine = next_wind_turbine
        self.distance_next_wind_turbine = distance_next_wind_turbine
        self.bloc_type = bloc_type

    def __eq__(self, other):
        return self.next_stone == other.next_stone and self.next_wind_turbine == other.next_wind_turbine and self.bloc_type == other.bloc_type

    def to_tuple(self):
        return self.next_stone.to_value(), self.next_wind_turbine.to_value(), self.distance_next_wind_turbine, self.bloc_type
