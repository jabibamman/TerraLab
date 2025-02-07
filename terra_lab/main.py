import time

import pygame
from terra_lab.envs import EcoEnv
from terra_lab.envs.action import Action
from terra_lab.envs.agent import Agent
from terra_lab.envs.env import Env
from terra_lab.rl.ai_agent import AIAgent

AI_MODE = False

ACTION_MAPPING = {
    pygame.K_p: Action.PLACE_WIND_TURBINE.value,
    pygame.K_u: Action.PLACE_IRRIGATOR.value,
    pygame.K_r: Action.PLACE_PURIFIER.value,
    pygame.K_DOWN: Action.DOWN.value,
    pygame.K_UP: Action.UP.value,
    pygame.K_RIGHT: Action.RIGHT.value,
    pygame.K_LEFT: Action.LEFT.value,
}

def handle_action(event_key, map_instance):
    """
    Handles key presses for performing actions on the map.
    Returns the updated action type or None if no action is performed.
    """
    action = ACTION_MAPPING.get(event_key)
    if action:
        map_instance.step(action)

def main():
    """Main function to run the EcoEnv game."""
    env = Env()

    if AI_MODE:
        agent = AIAgent(env)
        env.set_agent(agent)
        env.step(Action.PLACE_WIND_TURBINE)

    else:
        agent = AIAgent(env)
        env.set_agent(agent)
        map_instance = EcoEnv(env)

        pygame.key.set_repeat(200, 50)

        done = False
        while not done:
            map_instance.render()
            map_instance.grass_animation_count += 1
            map_instance.grass_animation_count %= 210

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         done = True
            #     elif event.type == pygame.KEYDOWN:
            #         handle_action(event.key, map_instance)
            action, reward = agent.do()
            print(f'Action: {action}\tReward: {reward}\tScore: {agent.score}\tPosition: {agent.position}')
            print(agent.qtable)
            time.sleep(1)
        map_instance.close()


if __name__ == "__main__":
    main()
