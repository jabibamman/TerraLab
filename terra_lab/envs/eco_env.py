import gym
from gym import spaces
import numpy as np
import pygame
from terra_lab.utils.enums import MACHINE_TYPE, MAP_STATES

class EcoEnv(gym.Env):
    """
    Un environnement de base pour un jeu écologique avec un rendu graphique PyGame.
    
    - action_space (0 = planter, 1 = purifier, 2 = restaurer)
    """
    
    def __init__(self):
        super(EcoEnv, self).__init__()
        
        self.grid_size = 20
        self.cell_size = 40
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        
        self.observation_space = spaces.Box(low=0, high=2, shape=(self.grid_size, self.grid_size), dtype=np.int32)
        self.action_space = spaces.Discrete(3)
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.cell_size * self.grid_size, self.cell_size * self.grid_size))
        pygame.display.set_caption("EcoEnv")   

        
        self.current_action = 0 


    def reset(self):
        """
        Réinitialise l'environnement et retourne l'état initial.
        """
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        return self.state
    
    def checkIfEnergy(self, row, col):
        effect_size = MACHINE_TYPE.WIND_TURBINE.value["range"]
        for i in range(1-effect_size,effect_size):
            for y in range(1-effect_size,effect_size):
                if 0 <= row-i < self.grid_size and 0 <= col-y < self.grid_size:
                    if self.state[row-i,col-y] == 2:
                        return True

        return False
    
    def createFertileDirt(self, row, col):
        effect_size = MACHINE_TYPE.PURIFIER.value["range"]
        for i in range(1-effect_size,effect_size):
            for y in range(1-effect_size,effect_size):
                if 0 <= row-i < self.grid_size and 0 <= col-y < self.grid_size:
                    if self.state[row-i,col-y] == MAP_STATES.UNFERTILE_DIRT.value["value"]:
                        self.state[row-i,col-y] = MAP_STATES.FERTILE_DIRT.value["value"]
    
    def createGrass(self, row, col):
        effect_size = MACHINE_TYPE.IRRIGATOR.value["range"]
        for i in range(1-effect_size,effect_size):
            for y in range(1-effect_size,effect_size):
                if 0 <= row-i < self.grid_size and 0 <= col-y < self.grid_size:
                    if self.state[row-i,col-y] == MAP_STATES.FERTILE_DIRT.value["value"]:
                        self.state[row-i,col-y] = MAP_STATES.GRASS.value["value"]

    def step(self, row, col):
        """
        Applique l'action courante à la cellule spécifique (row, col).
        
        - row, col : Coordonnées de la cellule dans la grille
        - action (0 = planter, 1 = purifier, 2 = restaurer)
        """
        action = self.current_action

        if action == MACHINE_TYPE.WIND_TURBINE.value["value"]:  
            if self.state[row, col] == MAP_STATES.ROCK.value["value"]:  
                self.state[row, col] = MAP_STATES.WIND_TURBINE.value["value"]
        elif action == MACHINE_TYPE.PURIFIER.value["value"]:  
            if self.checkIfEnergy(row,col) and self.state[row, col] != MAP_STATES.WIND_TURBINE.value["value"] :
                self.state[row, col] = MAP_STATES.PURIFIER.value["value"]
                self.createFertileDirt(row, col)
        elif action == MACHINE_TYPE.IRRIGATOR.value["value"]:  
            if self.state[row, col] == MAP_STATES.FERTILE_DIRT.value["value"]:  
                self.state[row, col] = MAP_STATES.IRRIGATOR.value["value"]
                self.createGrass(row, col)

        return self.state

    def to_isometric(self, row, col):
        """
        Convertit les coordonnées de la grille en coordonnées isométriques.
        """
        iso_x = (col - row) * (self.cell_size // 2) + (self.grid_size * self.cell_size // 2)
        iso_y = (col + row) * (self.cell_size // 4)
        return iso_x, iso_y
    
    def from_isometric(self, x, y):
        """
        Convertit les coordonnées isométriques (x, y) de l'écran en
        coordonnées de grille (row, col).
        """
        grid_x = ((x - (self.grid_size * self.cell_size // 2)) / (self.cell_size // 2) + (y / (self.cell_size // 4))) / 2
        grid_y = ((y / (self.cell_size // 4)) - (x - (self.grid_size * self.cell_size // 2)) / (self.cell_size // 2)) / 2
        row = int(grid_y)
        col = int(grid_x)
        return row, col
    

    def render(self, current_pos):
        """
        Affiche l'état actuel de l'environnement sous forme de grille isométrique avec PyGame.
        """
        self.screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 36)

        action_text = f"Machine choisi: {self.current_action}"
        if self.current_action == 0 :
            action_text = f"Machine choisi: (aucune)"
        text_surface = font.render(action_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 500))
        text1 = "P = éolienne (ne peut être posé que sur des rochers)"
        text_surface = font.render(text1, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 550))
        text2 = "R = purificateur (ne peut être posé que proche d'éoliennes)"
        text_surface = font.render(text2, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 600))
        text3 = "U = irrigateur (ne peut être posé que sur de la terre fertile)"
        text_surface = font.render(text3, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 650))
        text4 = f"Position actuelle : {current_pos}"
        text_surface = font.render(text4, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = MAP_STATES.UNFERTILE_DIRT.value["color"]
                iso_x, iso_y = self.to_isometric(row, col)
                points = [
                    (iso_x, iso_y - self.cell_size // 4),
                    (iso_x + self.cell_size // 2, iso_y),
                    (iso_x, iso_y + self.cell_size // 4),
                    (iso_x - self.cell_size // 2, iso_y)
                ]
                if self.state[row, col] == MAP_STATES.ROCK.value["value"]:
                    color = MAP_STATES.ROCK.value["color"]
                elif self.state[row, col] == MAP_STATES.WIND_TURBINE.value["value"]:
                    color = MAP_STATES.WIND_TURBINE.value["color"]
                elif self.state[row, col] == MAP_STATES.PURIFIER.value["value"]:
                    color = MAP_STATES.PURIFIER.value["color"]
                elif self.state[row, col] == MAP_STATES.FERTILE_DIRT.value["value"]:
                    color = MAP_STATES.FERTILE_DIRT.value["color"]
                elif self.state[row, col] == MAP_STATES.IRRIGATOR.value["value"]:
                    color = MAP_STATES.IRRIGATOR.value["color"]
                elif self.state[row, col] == MAP_STATES.GRASS.value["value"]:
                    color = MAP_STATES.GRASS.value["color"]

                mous_x, mous_y = pygame.mouse.get_pos()

                if iso_x - self.cell_size // 4 < mous_x < iso_x + self.cell_size // 4 and iso_y - self.cell_size // 4 < mous_y < iso_y + self.cell_size // 4:

                    if True :
                        if self.current_action == MACHINE_TYPE.WIND_TURBINE.value["value"] :
                            color = MAP_STATES.WIND_TURBINE.value["color"]
                        if self.current_action == MACHINE_TYPE.PURIFIER.value["value"] :
                            color = MAP_STATES.PURIFIER.value["color"]
                        if self.current_action == MACHINE_TYPE.IRRIGATOR.value["value"] :
                            color = MAP_STATES.IRRIGATOR.value["color"]
                    else :
                        points = [
                            (iso_x, iso_y - self.cell_size // 4 + 2),
                            (iso_x + self.cell_size // 2 - 3, iso_y),
                            (iso_x, iso_y + self.cell_size // 4 - 2),
                            (iso_x - self.cell_size // 2 + 3, iso_y)
                        ]
                
                pygame.draw.polygon(self.screen, color, points)

                current_iso_x, current_iso_y = self.to_isometric(current_pos[0], current_pos[1])

                pygame.draw.circle(self.screen, (0,0,0), [current_iso_x, current_iso_y], 5)
        
        pygame.display.flip()

    def close(self):
        """
        Ferme l'affichage PyGame.
        """
        pygame.quit()