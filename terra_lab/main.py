import pygame
from terra_lab.envs import EcoEnv
from terra_lab.envs.env import Env
from terra_lab.utils.enums import MACHINE_TYPE


def initialize_map(map_instance):
    """Initializes the map with some predefined state."""
    initial_positions = [(2, 2), (8, 2), (2, 8), (10, 10)]
    for x, y in initial_positions:
        map_instance.state[x, y] = 1


def handle_action(event_key, map_instance, x, y):
    """
    Handles key presses for performing actions on the map.
    Returns the updated action type or None if no action is performed.
    """
    action_mapping = {
        pygame.K_p: MACHINE_TYPE.WIND_TURBINE.value.name,
        pygame.K_u: MACHINE_TYPE.IRRIGATOR.value.name,
        pygame.K_r: MACHINE_TYPE.PURIFIER.value.name,
    }

    action = action_mapping.get(event_key)
    if action:
        map_instance.current_action = action
        map_instance.step(x, y)


def handle_movement(event_key, x, y, grid_size):
    """
    Handles movement key presses to update the current position.
    Returns the updated x and y coordinates.
    """
    if event_key == pygame.K_DOWN:
        y = (y + 1) % grid_size
    elif event_key == pygame.K_UP:
        y = (y - 1) % grid_size
    elif event_key == pygame.K_RIGHT:
        x = (x - 1) % grid_size
    elif event_key == pygame.K_LEFT:
        x = (x + 1) % grid_size
    return x, y


def main():
    """Main function to run the EcoEnv game."""
    env = Env()
    map_instance = EcoEnv(env)

    obs = map_instance.agent.env.reset()
    done = False

    initialize_map(map_instance.agent.env)

    current_x, current_y = 0, 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                handle_action(event.key, map_instance, current_x, current_y)
                
                current_x, current_y = handle_movement(
                    event.key, current_x, current_y, map_instance.agent.env.grid_size
                )

        map_instance.render([current_x, current_y])

    map_instance.close()


if __name__ == "__main__":
    main()
