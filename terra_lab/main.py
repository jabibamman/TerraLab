import pygame
from terra_lab.envs import EcoEnv


def main():
    env = EcoEnv()
    
    obs = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        reward = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    env.current_action = 0 
                elif event.key == pygame.K_u:
                    env.current_action = 1
                elif event.key == pygame.K_r:
                    env.current_action = 2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = env.from_isometric(x, y)
                if 0 <= row < env.grid_size and 0 <= col < env.grid_size:
                    obs, reward, done, info = env.step(row, col)
                    total_reward += reward
        
        env.render()
        
    print(f"Fin de l'épisode avec une récompense totale de : {total_reward}")
    env.close()

if __name__ == "__main__":
    main()