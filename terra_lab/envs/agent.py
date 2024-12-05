from terra_lab.utils.enums import MAP_STATES, MACHINE_TYPE

START_LEAVES = 300
LEAVES_PER_GREEN_SQUARE = 5


class Agent:
    def __init__(self, env):
        self.leaves = START_LEAVES
        self.env = env

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
        return self.leaves > amount

    def place_wind_turbine(self, row, col):
        if not self.can_pay_leaves(MACHINE_TYPE.WIND_TURBINE.value.price):
            # Handle not enought leaves
            return

        if self.env.state[row, col] == MAP_STATES.ROCK.value.value:
            self.pay_leaves(MACHINE_TYPE.WIND_TURBINE.value.price)
            self.env.state[row, col] = MAP_STATES.WIND_TURBINE.value.value

    def place_purifier(self, row, col):
        if not self.can_pay_leaves(MACHINE_TYPE.PURIFIER.value.price):
            # Handle not enought leaves
            return

        if self.env.check_if_energy(row, col) and self.env.state[row, col] != MAP_STATES.WIND_TURBINE.value.value:
            self.pay_leaves(MACHINE_TYPE.PURIFIER.value.price)
            self.env.state[row, col] = MAP_STATES.PURIFIER.value.value
            self.env.apply_effect(
                row, col,
                MACHINE_TYPE.PURIFIER.value.range,
                lambda cell: cell == MAP_STATES.UNFERTILE_DIRT.value.value,
                MAP_STATES.FERTILE_DIRT.value.value
            )

    def place_irrigator(self, row, col):
        if not self.can_pay_leaves(MACHINE_TYPE.IRRIGATOR.value.price):
            # Handle not enought leaves
            return

        if self.env.state[row, col] == MAP_STATES.FERTILE_DIRT.value.value:
            self.pay_leaves(MACHINE_TYPE.IRRIGATOR.value.price)
            last_grass_count = self.env.count_grass()
            self.env.state[row, col] = MAP_STATES.IRRIGATOR.value.value
            self.env.apply_effect(
                row, col,
                MACHINE_TYPE.IRRIGATOR.value.range,
                lambda cell: cell == MAP_STATES.FERTILE_DIRT.value.value,
                MAP_STATES.GRASS.value.value
            )
            current_grass_count = self.env.count_grass()
            added_grass = current_grass_count - last_grass_count
            self.gain_leaves(added_grass)
