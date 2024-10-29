import random
from terra_lab.envs import EcoEnv
import pygame

def main():
    env = EcoEnv()
    
    obs = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        # (0 = planter, 1 = purifier, 2 = restaurer)
        action = random.choice([0, 1, 2])
        obs, reward, done, info = env.step(action)
        
        env.render()
        
        total_reward += reward

    print(f"Fin de l'épisode avec une récompense totale de : {total_reward}")
    env.close()

if __name__ == "__main__":
    main()