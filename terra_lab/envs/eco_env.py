import gym
from gym import spaces
import numpy as np
import pygame
import random
from terra_lab.utils.enums import MACHINE_TYPE, MAP_STATES


class EcoEnv(gym.Env):
    """
    Un environnement de jeu écologique avec rendu graphique PyGame.
    """

    def __init__(self):
        super(EcoEnv, self).__init__()
        
        self.grid_size = 40
        self.cell_size = 20
        self.grass_animation_count = 0
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)

        self.sprites = {
            MAP_STATES.ROCK.value["value"]: pygame.image.load("assets/sprites/Rock.png"),
            MAP_STATES.WIND_TURBINE.value["value"]: pygame.image.load("assets/sprites/Turbine.png"),
            MAP_STATES.PURIFIER.value["value"]: pygame.image.load("assets/sprites/Toxin_Scrubber.png"),
            MAP_STATES.IRRIGATOR.value["value"]: pygame.image.load("assets/sprites/Irrigator.png"),
            MAP_STATES.UNFERTILE_DIRT.value["value"]: pygame.image.load("assets/sprites/Wasteland.png"),
            MAP_STATES.FERTILE_DIRT.value["value"]: pygame.image.load("assets/sprites/dirt1.png"),
            MAP_STATES.GRASS.name: pygame.image.load("assets/sprites/grass8.png"),
        }

        self.grass_sprites = {
            1: pygame.image.load("assets/sprites/grass1.png"),
            2: pygame.image.load("assets/sprites/grass2.png"),
            3: pygame.image.load("assets/sprites/grass3.png"),
            4: pygame.image.load("assets/sprites/grass4.png"),
            5: pygame.image.load("assets/sprites/grass5.png"),
            6: pygame.image.load("assets/sprites/grass6.png"),
            7: pygame.image.load("assets/sprites/grass7.png"),
            8: pygame.image.load("assets/sprites/grass8.png"),
            9: pygame.image.load("assets/sprites/grass9.png"),
            10: pygame.image.load("assets/sprites/grass10.png"),
        }

        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (self.cell_size, self.cell_size))

        for key in self.grass_sprites:
            self.grass_sprites[key] = pygame.transform.scale(self.grass_sprites[key], (self.cell_size, self.cell_size))


        self.observation_space = spaces.Box(
            low=0, high=2, shape=(self.grid_size, self.grid_size), dtype=np.int32
        )
        self.action_space = spaces.Discrete(3)

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.cell_size * self.grid_size, self.cell_size * self.grid_size - 150)
        )
        pygame.display.set_caption("EcoEnv")

        self.current_action = 0 

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
        effect_range = MACHINE_TYPE.WIND_TURBINE.value["range"]
        for dx in range(1 - effect_range, effect_range):
            for dy in range(1 - effect_range, effect_range):
                nx, ny = row - dx, col - dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if self.state[nx, ny] == MAP_STATES.WIND_TURBINE.value["value"]:
                        return True
        return False

    def step(self, row, col):
        """Applique l'action courante à la cellule spécifiée."""
        action = self.current_action
        cell_state = self.state[row, col]

        if action == MACHINE_TYPE.WIND_TURBINE.value["value"]:
            if cell_state == MAP_STATES.ROCK.value["value"]:
                self.state[row, col] = MAP_STATES.WIND_TURBINE.value["value"]

        elif action == MACHINE_TYPE.PURIFIER.value["value"]:
            if self.check_if_energy(row, col) and cell_state != MAP_STATES.WIND_TURBINE.value["value"]:
                self.state[row, col] = MAP_STATES.PURIFIER.value["value"]
                self.apply_effect(
                    row, col,
                    MACHINE_TYPE.PURIFIER.value["range"],
                    lambda cell: cell == MAP_STATES.UNFERTILE_DIRT.value["value"],
                    MAP_STATES.FERTILE_DIRT.value["value"]
                )

        elif action == MACHINE_TYPE.IRRIGATOR.value["value"]:
            if cell_state == MAP_STATES.FERTILE_DIRT.value["value"]:
                self.state[row, col] = MAP_STATES.IRRIGATOR.value["value"]
                self.apply_effect(
                    row, col,
                    MACHINE_TYPE.IRRIGATOR.value["range"],
                    lambda cell: cell == MAP_STATES.FERTILE_DIRT.value["value"],
                    MAP_STATES.GRASS.value["value"]
                )

        return self.state

    def to_isometric(self, row, col):
        """Convertit des coordonnées de grille en coordonnées isométriques."""
        iso_x = (col - row) * (self.cell_size // 2) + (self.grid_size * self.cell_size // 2)
        iso_y = (col + row) * (self.cell_size // 4)
        return iso_x, iso_y

    def render(self, current_pos):
        """Affiche l'état actuel de l'environnement."""

        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)

        texts = [
            f"Position actuelle: {current_pos}",
            f"Machine choisie: {self.current_action}",
            "P = éolienne (se place sur des rochers)",
            "R = purificateur (proche d'éoliennes)",
            "U = irrigateur (sur de la terre fertile)",
        ]
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 400 + i * 50))

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.state[row, col] == MAP_STATES.WIND_TURBINE.value["value"] or self.state[row, col] == MAP_STATES.IRRIGATOR.value["value"] : 
                    color = self.get_cell_color(self.state[row, col])
                    iso_x, iso_y = self.to_isometric(row, col)

                    points = [
                        (iso_x, iso_y - self.cell_size // 4),
                        (iso_x + self.cell_size // 2 +5, iso_y),
                        (iso_x, iso_y + self.cell_size // 4 +5),
                        (iso_x - self.cell_size // 2, iso_y),
                    ]

                    pygame.draw.polygon(self.screen, color, points)


                cell_value = self.state[row, col]
                iso_x, iso_y = self.to_isometric(row, col)
                if cell_value != MAP_STATES.GRASS.value["value"] : 
                    sprite = self.sprites.get(cell_value, None)
                else:
                    if self.grass_animation_count // 10 == col%20 or self.grass_animation_count // 10 == col%20 + 2 or self.grass_animation_count // 10 == col%20 + 3 :
                        sprite = self.grass_sprites.get(3, None)
                    else :
                        sprite = self.grass_sprites.get(1, None)


                if sprite:
                    if self.state[row, col] == MAP_STATES.UNFERTILE_DIRT.value["value"] or self.state[row, col] == MAP_STATES.FERTILE_DIRT.value["value"] or self.state[row, col] == MAP_STATES.GRASS.value["value"] : 
                        sprite_rect = sprite.get_rect(center=(iso_x, iso_y+3))
                    elif self.state[row, col] == MAP_STATES.WIND_TURBINE.value["value"] : 
                        sprite_rect = sprite.get_rect(center=(iso_x, iso_y-5))
                    else :
                        sprite_rect = sprite.get_rect(center=(iso_x, iso_y))
                    self.screen.blit(sprite, sprite_rect)  
                    
                    

        iso_x, iso_y = self.to_isometric(current_pos[0], current_pos[1])
        pygame.draw.circle(self.screen, (0, 0, 0), [iso_x, iso_y], 3)

        pygame.display.flip()

    def get_cell_color(self, cell_value):
        """Retourne la couleur correspondant à l'état d'une cellule."""
        for state in MAP_STATES:
            if cell_value == state.value["value"]:
                return state.value["color"]
        return MAP_STATES.UNFERTILE_DIRT.value["color"]

    def is_mouse_over(self, iso_x, iso_y):
        """Vérifie si la souris survole une cellule donnée."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
            iso_x - self.cell_size // 4 < mouse_x < iso_x + self.cell_size // 4 and
            iso_y - self.cell_size // 4 < mouse_y < iso_y + self.cell_size // 4
        )

    def close(self):
        """Ferme l'affichage PyGame."""
        pygame.quit()
