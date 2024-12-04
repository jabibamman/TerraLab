import gym
from gym import spaces
import numpy as np
import pygame

from terra_lab.envs.agent import Agent
from terra_lab.utils.enums import MACHINE_TYPE, MAP_STATES


class EcoEnv(gym.Env):
    """
    Un environnement de jeu écologique avec rendu graphique PyGame.
    """

    def __init__(self, env):
        super(EcoEnv, self).__init__()

        self.agent = Agent(env)

        self.cell_size = 20

        self.sprites = {
            MAP_STATES.ROCK.value.value: pygame.image.load("assets/sprites/Rock.png"),
            MAP_STATES.WIND_TURBINE.value.value: pygame.image.load("assets/sprites/Turbine.png"),
            MAP_STATES.PURIFIER.value.value: pygame.image.load("assets/sprites/Toxin_Scrubber.png"),
            MAP_STATES.IRRIGATOR.value.value: pygame.image.load("assets/sprites/Irrigator.png"),
            MAP_STATES.UNFERTILE_DIRT.value.value: pygame.image.load("assets/sprites/Wasteland.png"),
            MAP_STATES.FERTILE_DIRT.value.value: pygame.image.load("assets/sprites/Soil.png"),
            MAP_STATES.GRASS.value.value: pygame.image.load("assets/sprites/Greenery.png"),
        }

        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (self.cell_size, self.cell_size))

        self.observation_space = spaces.Box(
            low=0, high=2, shape=(self.agent.env.grid_size, self.agent.env.grid_size), dtype=np.int32
        )
        self.action_space = spaces.Discrete(3)

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.cell_size * self.agent.env.grid_size, self.cell_size * self.agent.env.grid_size - 150)
        )
        pygame.display.set_caption("EcoEnv")

        self.current_action = 0

    def step(self, row, col):
        """Applique l'action courante à la cellule spécifiée."""
        action = self.current_action

        if action == MACHINE_TYPE.WIND_TURBINE.value.name:
            self.agent.place_wind_turbine(row, col)
        elif action == MACHINE_TYPE.PURIFIER.value.name:
            self.agent.place_purifier(row, col)
        elif action == MACHINE_TYPE.IRRIGATOR.value.name:
            self.agent.place_irrigator(row, col)

        return self.agent.env.state

    def to_isometric(self, row, col):
        """Convertit des coordonnées de grille en coordonnées isométriques."""
        iso_x = (col - row) * (self.cell_size // 2) + (self.agent.env.grid_size * self.cell_size // 2)
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

        for row in range(self.agent.env.grid_size):
            for col in range(self.agent.env.grid_size):
                if self.agent.env.state[row, col] == MAP_STATES.WIND_TURBINE.value.value or self.agent.env.state[row, col] == MAP_STATES.IRRIGATOR.value.value :
                    color = self.get_cell_color(self.agent.env.state[row, col])
                    iso_x, iso_y = self.to_isometric(row, col)

                    points = [
                        (iso_x, iso_y - self.cell_size // 4),
                        (iso_x + self.cell_size // 2 +5, iso_y),
                        (iso_x, iso_y + self.cell_size // 4 +5),
                        (iso_x - self.cell_size // 2, iso_y),
                    ]

                    pygame.draw.polygon(self.screen, color, points)


                cell_value = self.agent.env.state[row, col]
                iso_x, iso_y = self.to_isometric(row, col)
                sprite = self.sprites.get(cell_value, None)

                if sprite:
                    if self.agent.env.state[row, col] == MAP_STATES.UNFERTILE_DIRT.value.value or self.agent.env.state[row, col] == MAP_STATES.FERTILE_DIRT.value.value or self.agent.env.state[row, col] == MAP_STATES.GRASS.value.value :
                        sprite_rect = sprite.get_rect(center=(iso_x, iso_y+3))
                    elif self.agent.env.state[row, col] == MAP_STATES.WIND_TURBINE.value.value :
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
            if cell_value == state.value.value:
                return state.value.color
        return MAP_STATES.UNFERTILE_DIRT.value.color

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
