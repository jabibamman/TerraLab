from abc import ABC, abstractmethod

class AbstractAgent(ABC):
    @abstractmethod
    def reset(self):
        pass
    def move_up(self):
        pass
    def move_down(self):
        pass
    def move_left(self):
        pass
    def move_right(self):
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
    def place_wind_turbine(self):
        pass
    def place_purifier(self):
        pass
    def place_irrigator(self):
        pass