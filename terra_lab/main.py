import pygame
from terra_lab.envs import EcoEnv
from terra_lab.envs.env import Env
from terra_lab.utils.enums import MACHINE_TYPE


ACTION_MAPPING = {
    pygame.K_p: MACHINE_TYPE.WIND_TURBINE.value.name,
    pygame.K_u: MACHINE_TYPE.IRRIGATOR.value.name,
    pygame.K_r: MACHINE_TYPE.PURIFIER.value.name,
}

def handle_action(event_key, map_instance):
    """
    Handles key presses for performing actions on the map.
    Returns the updated action type or None if no action is performed.
    """
    action = ACTION_MAPPING.get(event_key)
    if action:
        map_instance.current_action = action
        map_instance.step()


def handle_movement(event_key, map_instance):
    """
    Handles movement key presses to update the current position.
    Returns the updated x and y coordinates.
    """
    if event_key == pygame.K_DOWN:
        map_instance.agent.move_down()
    elif event_key == pygame.K_UP:
        map_instance.agent.move_up()
    elif event_key == pygame.K_RIGHT:
        map_instance.agent.move_right()
    elif event_key == pygame.K_LEFT:
        map_instance.agent.move_left()


def main():
    """Main function to run the EcoEnv game."""
    env = Env()
    map_instance = EcoEnv(env)

    pygame.key.set_repeat(200, 50)

    done = False
    while not done:
        map_instance.grass_animation_count += 1
        if map_instance.grass_animation_count > 210:
            map_instance.grass_animation_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                handle_action(event.key, map_instance)
                handle_movement(event.key, map_instance)

        map_instance.render()
    map_instance.close()


if __name__ == "__main__":
    main()
