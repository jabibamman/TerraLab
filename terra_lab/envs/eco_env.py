import gym
from gym import spaces
import numpy as np
import pygame

from terra_lab.envs.action import Action
from terra_lab.utils.enums import MACHINE_TYPE, MAP_STATES


class EcoEnv(gym.Env):
    """
    Un environnement de jeu écologique avec rendu graphique PyGame.
    """

    def __init__(self, env):
        super(EcoEnv, self).__init__()

        self.env = env
        self.agent = self.env.agent

        self.cell_size = 20
        self.grass_animation_count = 0
        pygame.init()

        self.sprites = {
            MAP_STATES.ROCK.value.value: pygame.image.load("assets/sprites/Rock.png"),
            MAP_STATES.WIND_TURBINE.value.value: pygame.image.load("assets/sprites/Turbine.png"),
            MAP_STATES.PURIFIER.value.value: pygame.image.load("assets/sprites/Toxin_Scrubber.png"),
            MAP_STATES.IRRIGATOR.value.value: pygame.image.load("assets/sprites/Irrigator.png"),
            MAP_STATES.UNFERTILE_DIRT.value.value: pygame.image.load("assets/sprites/Wasteland.png"),
            MAP_STATES.FERTILE_DIRT.value.value: pygame.image.load("assets/sprites/dirt1.png"),
            MAP_STATES.GRASS.name: pygame.image.load("assets/sprites/grass8.png"),
           20: pygame.image.load("assets/sprites/hand.png"),
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
            low=0, high=2, shape=(self.env.grid_size, self.env.grid_size), dtype=np.int32
        )
        self.action_space = spaces.Discrete(3)

        self.screen = pygame.display.set_mode(
            (self.cell_size * self.env.grid_size, self.cell_size * self.env.grid_size - 150)
        )
        pygame.display.set_caption("EcoEnv")

    def step(self, action: Action):
        self.env.step(action)

    def reset(self):
        self.env.reset()

    def to_isometric(self, row: int, col: int) -> tuple[int, int]:
        """Convertit des coordonnées de grille en coordonnées isométriques."""
        iso_x = (col - row) * (self.cell_size // 2) + (self.env.grid_size * self.cell_size // 2)
        iso_y = (col + row) * (self.cell_size // 4)
        return iso_x, iso_y

    def render(self):
        """Affiche l'état actuel de l'environnement."""
        print('RENDERING')
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)

        texts = [
            f"Feuilles (argent): {self.agent.leaves}",
            f"P = éolienne (se place sur des rochers) prix: {MACHINE_TYPE.WIND_TURBINE.value.price}",
            f"R = purificateur (proche d'éoliennes) prix: {MACHINE_TYPE.PURIFIER.value.price}",
            f"U = irrigateur (sur de la terre fertile) prix: {MACHINE_TYPE.IRRIGATOR.value.price}",
        ]
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 400 + i * 50))

        for row in range(self.env.grid_size):
            for col in range(self.env.grid_size):
                if self.env.state[row, col] == MAP_STATES.WIND_TURBINE.value.value or self.env.state[row, col] == MAP_STATES.IRRIGATOR.value.value :
                    color = self.get_cell_color(self.env.state[row, col])
                    iso_x, iso_y = self.to_isometric(row, col)

                    points = [
                        (iso_x, iso_y - self.cell_size // 4),
                        (iso_x + self.cell_size // 2 +5, iso_y),
                        (iso_x, iso_y + self.cell_size // 4 +5),
                        (iso_x - self.cell_size // 2, iso_y),
                    ]

                    pygame.draw.polygon(self.screen, color, points)

                cell_value = self.env.state[row, col]
                iso_x, iso_y = self.to_isometric(row, col)
                if cell_value != MAP_STATES.GRASS.value.value :
                    sprite = self.sprites.get(cell_value, None)
                else:
                    if self.grass_animation_count // 10 == col%20 or self.grass_animation_count // 10 == col%20 + 2 or self.grass_animation_count // 10 == col%20 + 3 :
                        sprite = self.grass_sprites.get(3, None)
                    else :
                        sprite = self.grass_sprites.get(1, None)


                if sprite:
                    if self.env.state[row, col] == MAP_STATES.UNFERTILE_DIRT.value.value or self.env.state[row, col] == MAP_STATES.FERTILE_DIRT.value.value or self.env.state[row, col] == MAP_STATES.GRASS.value.value :
                        sprite_rect = sprite.get_rect(center=(iso_x, iso_y+3))
                    elif self.env.state[row, col] == MAP_STATES.WIND_TURBINE.value.value :
                        sprite_rect = sprite.get_rect(center=(iso_x, iso_y-5))
                    else:
                        sprite_rect = sprite.get_rect(center=(iso_x, iso_y))
                    self.screen.blit(sprite, sprite_rect)  

        iso_x, iso_y = self.to_isometric(self.agent.position.x, self.agent.position.y)
        pygame.draw.circle(self.screen, (0, 0, 0), [iso_x, iso_y], 2)
        sprite = self.sprites.get(20, None)
        sprite_rect = sprite.get_rect(center=(iso_x+2, iso_y+10))
        self.screen.blit(sprite, sprite_rect)  
        

        pygame.display.flip()

    def get_cell_color(self, cell_value) -> tuple[int, int, int]:
        """Retourne la couleur correspondant à l'état d'une cellule."""
        for state in MAP_STATES:
            if cell_value == state.value.value:
                return state.value.color
        return MAP_STATES.UNFERTILE_DIRT.value.color

    def is_mouse_over(self, iso_x: int, iso_y: int) -> bool:
        """Vérifie si la souris survole une cellule donnée."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (
            iso_x - self.cell_size // 4 < mouse_x < iso_x + self.cell_size // 4 and
            iso_y - self.cell_size // 4 < mouse_y < iso_y + self.cell_size // 4
        )

    def close(self):
        """Ferme l'affichage PyGame."""
        pygame.quit()
