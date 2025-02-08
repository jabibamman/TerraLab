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

    @staticmethod
    def from_value(value: int):
        return Radar(
            up=bool(value & 1),
            down=bool(value & 2),
            left=bool(value & 4),
            right=bool(value & 8)
        )


class State:
    def __init__(self, next_rock: Radar, distance_next_wind_turbine: int, bloc_type: int):
        self.next_rock = next_rock
        self.distance_next_wind_turbine = distance_next_wind_turbine
        self.bloc_type = bloc_type

    def __eq__(self, other):
        return self.next_rock == other.next_rock and self.bloc_type == other.bloc_type

    def __hash__(self):
        return hash((self.next_rock, self.distance_next_wind_turbine, self.bloc_type))

    def __iter__(self):
        return iter(self.to_tuple())

    def __str__(self):
        return f"{self.next_rock.to_value()},{self.distance_next_wind_turbine},{self.bloc_type}"

    def to_tuple(self):
        return self.next_rock.to_value(), self.distance_next_wind_turbine, self.bloc_type

    @staticmethod
    def from_str(state_str):
        next_rock, distance_next_wind_turbine, block_type = state_str.split(",")
        return State(Radar.from_value(int(next_rock)), distance_next_wind_turbine, block_type)
