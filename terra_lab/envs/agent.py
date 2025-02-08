from terra_lab.envs.abstract_agent import AbstractAgent
from terra_lab.envs.action import Action, MOVES
from terra_lab.envs.env import Env
from terra_lab.envs.position import Position
from terra_lab.rl.reward import Reward
from terra_lab.utils.enums import MAP_STATES, MACHINE_TYPE

START_LEAVES = 500
LEAVES_PER_GREEN_SQUARE = 3


class Agent(AbstractAgent):
    def __init__(self, env: Env):
        self.leaves = START_LEAVES
        self.env = env
        self.position = Position(0, 0)
        self.score = 0

    def get_score(self):
        return self.score

    def reset(self):
        self.leaves = START_LEAVES
        self.position = Position(0, 0)

    def move_up(self) -> int:
        self.position += MOVES[Action.UP]
        self.position %= self.env.grid_size
        return Reward.MOVE.value
    def move_down(self) -> int:
        self.position += MOVES[Action.DOWN]
        self.position %= self.env.grid_size
        return Reward.MOVE.value
    def move_left(self) -> int:
        self.position += MOVES[Action.LEFT]
        self.position %= self.env.grid_size
        return Reward.MOVE.value
    def move_right(self) -> int:
        self.position += MOVES[Action.RIGHT]
        self.position %= self.env.grid_size
        return Reward.MOVE.value

    def has_win(self) -> bool:
        """ Renvoie True si le joueur a gagné """
        return self.env.count_grass() > ((self.env.grid_size ** 2) * 0.8)

    def has_lose(self) -> bool:
        """ Renvoie True si le joueur a perdu """
        if self.env.can_place_turbine() and self.can_pay_leaves(MACHINE_TYPE.WIND_TURBINE.value.price):
            return False
        elif self.can_pay_leaves(MACHINE_TYPE.PURIFIER.value.price):
            return False
        elif self.can_pay_leaves(MACHINE_TYPE.IRRIGATOR.value.price):
            return False
        return True

    def gain_leaves(self, nb_green_square: int) -> None:
        """ Gagne des feuilles pour chaque terrain vert obtenu """
        self.leaves += nb_green_square * LEAVES_PER_GREEN_SQUARE

    def pay_leaves(self, amount: int) -> bool:
        """
        Paye des feuilles pour acheter un batiment.
        Renvoie True si le joueur avait assez pour payer
        """
        if self.leaves < amount:
            return False
        self.leaves -= amount
        return True

    def can_pay_leaves(self, amount: int) -> bool:
        """ Vérifie si l'agent a assez d'argent pour payer le montant donné """
        return self.leaves >= amount

    def place_wind_turbine(self) -> int:
        if not self.can_pay_leaves(MACHINE_TYPE.WIND_TURBINE.value.price):
            return Reward.NOT_ENOUGHT_MONEY.value

        if self.env.state[self.position.to_tuple()] != MAP_STATES.ROCK.value.value:
            return Reward.WRONG_INPUT.value

        self.pay_leaves(MACHINE_TYPE.WIND_TURBINE.value.price)
        self.env.state[self.position.to_tuple()] = MAP_STATES.WIND_TURBINE.value.value
        return Reward.PLACE_WIND_TURBINE.value

    def place_purifier(self) -> int:
        if not self.can_pay_leaves(MACHINE_TYPE.PURIFIER.value.price):
            return Reward.NOT_ENOUGHT_MONEY.value

        if not self.env.check_if_energy(self.position.x, self.position.y) or self.env.state[self.position.to_tuple()] == MAP_STATES.WIND_TURBINE.value.value or self.env.state[self.position.to_tuple()] == MAP_STATES.IRRIGATOR.value.value:
            return Reward.WRONG_INPUT.value

        self.pay_leaves(MACHINE_TYPE.PURIFIER.value.price)
        self.env.state[self.position.to_tuple()] = MAP_STATES.PURIFIER.value.value
        added_dirt = self.env.apply_effect(
            self.position.x, self.position.y,
            MACHINE_TYPE.PURIFIER.value.range,
            lambda cell: cell == MAP_STATES.UNFERTILE_DIRT.value.value,
            MAP_STATES.FERTILE_DIRT.value.value
        )
        return (added_dirt * LEAVES_PER_GREEN_SQUARE) - MACHINE_TYPE.IRRIGATOR.value.price - MACHINE_TYPE.PURIFIER.value.price

    def place_irrigator(self) -> int:
        if not self.can_pay_leaves(MACHINE_TYPE.IRRIGATOR.value.price):
            return Reward.NOT_ENOUGHT_MONEY.value

        if self.env.state[self.position.to_tuple()] != MAP_STATES.FERTILE_DIRT.value.value:
            return Reward.WRONG_INPUT.value

        self.pay_leaves(MACHINE_TYPE.IRRIGATOR.value.price)
        self.env.state[self.position.to_tuple()] = MAP_STATES.IRRIGATOR.value.value
        added_grass = self.env.apply_effect(
            self.position.x, self.position.y,
            MACHINE_TYPE.IRRIGATOR.value.range,
            lambda cell: cell == MAP_STATES.FERTILE_DIRT.value.value,
            MAP_STATES.GRASS.value.value
        )
        self.gain_leaves(added_grass)
        return added_grass * LEAVES_PER_GREEN_SQUARE - MACHINE_TYPE.IRRIGATOR.value.price
