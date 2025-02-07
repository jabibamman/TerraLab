class Radar:
    def __init__(self, up: bool, down: bool, left: bool, right: bool):
        self.UP = up
        self.DOWN = down
        self.LEFT = left
        self.RIGHT = right

    def __eq__(self, other):
        return self.to_value() == other.to_value()

    def __hash__(self):
        return hash(self.to_value())

    def __str__(self):
        return f"({self.to_value()})"

    def to_value(self) -> int:
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
    def __init__(self, next_rock: Radar, next_wind_turbine: Radar, distance_next_wind_turbine: int, bloc_type: int):
        self.next_rock = next_rock
        self.next_wind_turbine = next_wind_turbine
        self.distance_next_wind_turbine = distance_next_wind_turbine
        self.bloc_type = bloc_type

    def __eq__(self, other):
        return self.next_rock == other.next_rock and self.next_wind_turbine == other.next_wind_turbine and self.bloc_type == other.bloc_type

    def __hash__(self):
        return hash((self.next_rock, self.next_wind_turbine, self.distance_next_wind_turbine, self.bloc_type))

    def __iter__(self):
        return iter(self.to_tuple())

    def __str__(self):
        return f"{self.to_tuple()}"

    def to_tuple(self):
        return self.next_rock.to_value(), self.next_wind_turbine.to_value(), self.distance_next_wind_turbine, self.bloc_type
