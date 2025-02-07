import numpy as np

from terra_lab.envs.abstract_agent import AbstractAgent
from terra_lab.envs.action import Action
from terra_lab.utils.enums import MACHINE_TYPE, MAP_STATES


class Env:
    def __init__(self):
        self.grid_size = 40
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.initialize_map()
        self.current_action = 0
        self.agent: AbstractAgent = None

    def set_agent(self, agent):
        self.agent = agent

    def reset(self):
        """ Réinitialise l'environnement """
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.initialize_map()
        self.agent.reset()

    def randomize_initial_rock_positions(self, count_rocks = 4):
        return [(5, 5), (5, 15), (5, 25), (5, 35), (15, 5), (15, 15), (15, 25), (15, 35), (25, 5), (25, 15), (25, 25), (25, 35)]


    def initialize_map(self):
        """Initializes the map with some predefined state."""
        initial_positions = self.randomize_initial_rock_positions()

        for x, y in initial_positions:
            self.state[x, y] = 1

    def apply_effect(self, row, col, effect_range, condition, new_state):
        """ Applique un effet sur les cellules dans une plage définie """
        for dx in range(1 - effect_range, effect_range):
            for dy in range(1 - effect_range, effect_range):
                nx, ny = row - dx, col - dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if condition(self.state[nx, ny]):
                        self.state[nx, ny] = new_state

    def check_if_energy(self, row: int, col: int) -> bool:
        """ Vérifie si une éolienne est à portée """
        effect_range = MACHINE_TYPE.WIND_TURBINE.value.range
        for dx in range(1 - effect_range, effect_range):
            for dy in range(1 - effect_range, effect_range):
                nx, ny = row - dx, col - dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if self.state[nx, ny] == MAP_STATES.WIND_TURBINE.value.value:
                        return True
        return False

    def count_grass(self) -> int:
        """ Compte le nombre d'herbes sur la map et renvoie cette valeur """
        count = 0
        for value in np.nditer(self.state):
            if value == MAP_STATES.GRASS.value.value:
                count += 1
        return count

    def step(self, action):
        """Applique l'action courante à la cellule spécifiée."""
        self.current_action = action

        action_mapping = {
            Action.UP.value: self.agent.move_up,
            Action.DOWN.value: self.agent.move_down,
            Action.LEFT.value: self.agent.move_left,
            Action.RIGHT.value: self.agent.move_right,
            Action.PLACE_WIND_TURBINE.value: self.agent.place_wind_turbine,
            Action.PLACE_IRRIGATOR.value: self.agent.place_irrigator,
            Action.PLACE_PURIFIER.value: self.agent.place_purifier,
        }

        agent_action = action_mapping[action]
        agent_action()

        if self.agent.has_win():
            # Win screen
            pass
        elif self.agent.has_lose():
            # Lose screen
            self.reset()
            pass

        return self.state

    def can_place_turbine(self) -> bool:
        """ Vérifie si une éolienne peut encore être placée """
        for value in np.nditer(self.state):
            if value == MAP_STATES.ROCK.value.value:
                return True
        return False
