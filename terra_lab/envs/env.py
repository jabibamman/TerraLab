import numpy as np

from terra_lab.utils.enums import MACHINE_TYPE, MAP_STATES


class Env:
    def __init__(self):
        self.grid_size = 40
        self.grass_count = 0
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)

    def reset(self):
        """Réinitialise l'environnement."""
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        return self.state

    def apply_effect(self, row, col, effect_range, condition, new_state):
        """
        Applique un effet sur les cellules dans une plage définie.
        """
        for dx in range(1 - effect_range, effect_range):
            for dy in range(1 - effect_range, effect_range):
                nx, ny = row - dx, col - dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if condition(self.state[nx, ny]):
                        self.state[nx, ny] = new_state

    def check_if_energy(self, row, col):
        """Vérifie si une éolienne est à portée."""
        effect_range = MACHINE_TYPE.WIND_TURBINE.value.range
        for dx in range(1 - effect_range, effect_range):
            for dy in range(1 - effect_range, effect_range):
                nx, ny = row - dx, col - dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if self.state[nx, ny] == MAP_STATES.WIND_TURBINE.value.value:
                        return True
        return False

    def update_grass_count(self):
        count = 0
        for value in np.nditer(self.state):
            if value == MAP_STATES.GRASS.value.value:
                count += 1
        self.grass_count = count

    def can_place_turbine(self):
        for value in np.nditer(self.state):
            if value == MAP_STATES.ROCK.value.value:
                return True
        return False
