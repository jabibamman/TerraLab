from abc import ABC, abstractmethod

class AbstractAgent(ABC):
    @abstractmethod
    def get_score(self):
        pass
    @abstractmethod
    def reset(self):
        pass
    @abstractmethod
    def move_up(self) -> int:
        pass
    @abstractmethod
    def move_down(self) -> int:
        pass
    @abstractmethod
    def move_left(self) -> int:
        pass
    @abstractmethod
    def move_right(self) -> int:
        pass
    @abstractmethod
    def has_win(self) -> bool:
        pass
    @abstractmethod
    def has_lose(self) -> bool:
        pass
    @abstractmethod
    def gain_leaves(self, nb_green_square: int) -> None:
        pass
    @abstractmethod
    def pay_leaves(self, amount: int) -> bool:
        pass
    @abstractmethod
    def can_pay_leaves(self, amount: int) -> bool:
        pass
    @abstractmethod
    def place_wind_turbine(self) -> int:
        pass
    @abstractmethod
    def place_purifier(self) -> int:
        pass
    @abstractmethod
    def place_irrigator(self) -> int:
        pass