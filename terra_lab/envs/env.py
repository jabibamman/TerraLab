import numpy as np

from terra_lab.utils.enums import MACHINE_TYPE, MAP_STATES


class Env:
    def __init__(self):
        self.grid_size = 40
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.initialize_map()

    def reset(self):
        """ Réinitialise l'environnement """
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.initialize_map()

    @staticmethod
    def generate_random_coordinates(lower_boundary, upper_boundary):
        return (
                np.int32(np.ceil(np.random.rand() * upper_boundary + lower_boundary)),
                np.int32(np.ceil(np.random.rand() * upper_boundary + lower_boundary)),
            )

    @staticmethod
    def distance(coordinate1, coordinate2):
        return np.abs(coordinate1 - coordinate2)

    @staticmethod
    def find_neighbors_with_invalid_distance(existing_rocks_coordinates, new_rock_coordinates, invalid_distance):
        """Returns a list of neighboring rocks that whose distance with the new_rock is less than or equal invalid_distance"""
        new_rock_x, new_rock_y = new_rock_coordinates
        neighbors = list(filter(lambda existing_rock_coordinates: Env.distance(new_rock_x, existing_rock_coordinates[0]) <= invalid_distance \
                                                                  or Env.distance(new_rock_y, existing_rock_coordinates[1]) <= invalid_distance
                        , existing_rocks_coordinates))

        return neighbors

    def randomize_initial_rock_positions(self, count_rocks = 4):
        wind_turbine_limits = (MACHINE_TYPE.WIND_TURBINE.value.range - 1, self.grid_size - MACHINE_TYPE.WIND_TURBINE.value.range)

        lower_boundary, upper_boundary = wind_turbine_limits
        upper_boundary -= lower_boundary
        initial_rock_positions = [Env.generate_random_coordinates(lower_boundary, upper_boundary)]
        for _ in range(count_rocks - 1):
            random_coordinates_within_limits = Env.generate_random_coordinates(lower_boundary, upper_boundary)

            # Checking that the new rock is not near any already generated rock
            invalid_neighbors = Env.find_neighbors_with_invalid_distance(initial_rock_positions, random_coordinates_within_limits, MACHINE_TYPE.WIND_TURBINE.value.range - 1)
            # if new rock is too close to an existing rock, generate new random coordinates until we get a valid result
            while len(invalid_neighbors) > 0:
                random_coordinates_within_limits = Env.generate_random_coordinates(lower_boundary, upper_boundary)
                invalid_neighbors = Env.find_neighbors_with_invalid_distance(initial_rock_positions, random_coordinates_within_limits, MACHINE_TYPE.WIND_TURBINE.value.range - 1)

            initial_rock_positions.append(random_coordinates_within_limits)

        return initial_rock_positions

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

    def can_place_turbine(self) -> bool:
        """ Vérifie si une éolienne peut encore être placée """
        for value in np.nditer(self.state):
            if value == MAP_STATES.ROCK.value.value:
                return True
        return False
