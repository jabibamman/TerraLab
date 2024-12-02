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

    current_x = 0
    current_y = 0
    current_pos = [current_x, current_y]
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    map.current_action = MACHINE_TYPE.WIND_TURBINE.value["value"]
                    map.step(current_x, current_y)
                elif event.key == pygame.K_u:
                    map.current_action = MACHINE_TYPE.IRRIGATOR.value["value"]
                    map.step(current_x, current_y)
                elif event.key == pygame.K_r:
                    map.current_action = MACHINE_TYPE.PURIFIER.value["value"]
                    map.step(current_x, current_y)
                elif event.key == pygame.K_DOWN:
                    current_y += 1 
                    if current_y >= map.grid_size:
                       current_y = 0
                    current_pos = [current_x, current_y]
                elif event.key == pygame.K_UP:
                    current_y -= 1 
                    if current_y < 0:
                       current_y = map.grid_size-1
                    current_pos = [current_x, current_y]
                elif event.key == pygame.K_RIGHT:
                    current_x -= 1 
                    if current_x < 0:
                       current_x = map.grid_size-1
                    current_pos = [current_x, current_y]
                elif event.key == pygame.K_LEFT:
                    current_x += 1 
                    if current_x >= map.grid_size:
                       current_x = 0
                    current_pos = [current_x, current_y]
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     x, y = event.pos
            #     row, col = map.from_isometric(x, y)
            #     if 0 <= row < map.grid_size and 0 <= col < map.grid_size:
            #         state = map.step(row, col)
        
        map.render(current_pos)
        
    map.close()

if __name__ == "__main__":
    main()