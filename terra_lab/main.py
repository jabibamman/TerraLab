import random
from terra_lab.envs import EcoEnv
import pygame
from terra_lab.utils.enums import MACHINE_TYPE

def main():
    map = EcoEnv()
    
    obs = map.reset()
    done = False

    #test
    map.state[2,2] = 1
    map.state[8,2] = 1
    map.state[2,8] = 1
    map.state[10,10] = 1


    
    
    while not done:
        reward = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    map.current_action = MACHINE_TYPE.WIND_TURBINE 
                elif event.key == pygame.K_u:
                   map.current_action = MACHINE_TYPE.IRRIGATOR 
                elif event.key == pygame.K_r:
                    map.current_action = MACHINE_TYPE.PURIFIER 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = map.from_isometric(x, y)
                if 0 <= row < map.grid_size and 0 <= col < map.grid_size:
                    state = map.step(row, col)
        
        map.render()
        
    map.close()

if __name__ == "__main__":
    main()