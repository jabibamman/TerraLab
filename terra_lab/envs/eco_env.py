import gym
from gym import spaces
import numpy as np
import pygame

class EcoEnv(gym.Env):
    """
    Un environnement de base pour un jeu écologique avec un rendu graphique PyGame.
    
    - action_space (0 = planter, 1 = purifier, 2 = restaurer)
    """
    
    def __init__(self):
        super(EcoEnv, self).__init__()
        
        self.grid_size = 10
        self.cell_size = 90  
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

    def step(self, row, col):
        """
        Applique l'action courante à la cellule spécifique (row, col).
        
        - row, col : Coordonnées de la cellule dans la grille
        - action (0 = planter, 1 = purifier, 2 = restaurer)
        """
        action = self.current_action  
        reward = 0

        if action == 0:  
            if self.state[row, col] == 0:  
                self.state[row, col] = 1
                reward = 10
        elif action == 1:  
            if self.state[row, col] == 0:  
                self.state[row, col] = 2
                reward = 5
        elif action == 2:  
            if self.state[row, col] == 1:  
                reward = 7

        
        done = np.all(self.state > 0)

        return self.state, reward, done, {}

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

    def render(self, mode="human"):
        """
        Affiche l'état actuel de l'environnement sous forme de grille isométrique avec PyGame.
        
        - color (gris = sol stérile, vert = végétation, bleu = eau)
        """
        self.screen.fill((0, 0, 0))

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = (200, 200, 200)
                if self.state[row, col] == 1:
                    color = (34, 139, 34)
                elif self.state[row, col] == 2:
                    color = (0, 191, 255)
                iso_x, iso_y = self.to_isometric(row, col)
                points = [
                    (iso_x, iso_y - self.cell_size // 4),
                    (iso_x + self.cell_size // 2, iso_y),
                    (iso_x, iso_y + self.cell_size // 4),
                    (iso_x - self.cell_size // 2, iso_y)
                ]
                
                pygame.draw.polygon(self.screen, color, points)
        
        pygame.display.flip()

    def close(self):
        """
        Ferme l'affichage PyGame.
        """
        pygame.quit()