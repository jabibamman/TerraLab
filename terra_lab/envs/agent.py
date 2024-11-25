from enum import Enum


class BuildingPrice(Enum):
    TURBINE = 75
    TOXIC_SCRUBBER = 50
    IRRIGATOR = 50

MIN_PRICE = min(
    BuildingPrice.TURBINE.value,
    BuildingPrice.TOXIC_SCRUBBER.value,
    BuildingPrice.IRRIGATOR.value
)

START_LEAVES = 100
LEAVES_PER_GREEN_SQUARE = 10


class Agent:
    def __init__(self):
        self.__leaves = START_LEAVES


    def has_player_lose(self) -> bool:
        """ Renvoie True si le joueur a perdu """
        return self.__leaves < MIN_PRICE

    def gain_leaves(self, nb_green_square: int) -> None:
        """ Gagne des feuilles pour chaque terrain vert obtenu """
        self.__leaves += nb_green_square * LEAVES_PER_GREEN_SQUARE

    def pay_leaves(self, amount: int) -> bool:
        """
        Paye des feuilles pour acheter un batiment.
        Renvoie True si le joueur avait assez pour payer
        """
        if self.__leaves < amount:
            return False
        self.__leaves -= amount
        return True
