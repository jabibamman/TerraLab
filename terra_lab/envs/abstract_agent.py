from abc import ABC, abstractmethod

class AbstractAgent(ABC):
    @abstractmethod
    def reset(self):
        pass
    def move_up(self) -> int:
        pass
    def move_down(self) -> int:
        pass
    def move_left(self) -> int:
        pass
    def move_right(self) -> int:
        pass
    def has_win(self) -> bool:
        pass
    def has_lose(self) -> bool:
        pass
    def gain_leaves(self, nb_green_square: int) -> None:
        pass
    def pay_leaves(self, amount: int) -> bool:
        pass
    def can_pay_leaves(self, amount: int) -> bool:
        pass
    def place_wind_turbine(self) -> int:
        pass
    def place_purifier(self) -> int:
        pass
    def place_irrigator(self) -> int:
        pass