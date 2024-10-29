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
        
        self.grid_size = 20
        self.cell_size = 90  
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        
        self.observation_space = spaces.Box(low=0, high=2, shape=(self.grid_size, self.grid_size), dtype=np.int32)
        self.action_space = spaces.Discrete(3)
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.cell_size * self.grid_size, self.cell_size * self.grid_size))
        pygame.display.set_caption("EcoEnv")

    def reset(self):
        """
        Réinitialise l'environnement et retourne l'état initial.
        """
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        return self.state

    def step(self, action):
        """
        Applique une action à une cellule aléatoire de la grille.

        - action (0 = planter, 1 = purifier, 2 = restaurer)
        - state (0 = sol stérile, 1 = végétation, 2 = eau)

        Toutes les cellules doivent être remplies pour terminer l'épisode.
        """
        row, col = np.random.randint(0, self.grid_size, size=2)

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

    def render(self, mode="human"):
        """
        Affiche l'état actuel de l'environnement sous forme de grille graphique avec PyGame.
        
        - color (gris = sol stérile, vert = végétation, bleu = eau)
        """
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = (200, 200, 200)
                if self.state[row, col] == 1:
                    color = (34, 139, 34)
                elif self.state[row, col] == 2:
                    color = (0, 191, 255)
                pygame.draw.rect(self.screen, color, pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
        
        pygame.display.flip()

    def close(self):
        """
        Ferme l'affichage PyGame.
        """
        pygame.quit()