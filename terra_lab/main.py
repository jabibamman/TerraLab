import time

import pygame
from terra_lab.envs import EcoEnv
from terra_lab.envs.action import Action
from terra_lab.envs.agent import Agent
from terra_lab.envs.env import Env
from terra_lab.mode import Mode
from terra_lab.rl.ai_agent import AIAgent



ACTION_MAPPING = {
    pygame.K_p: Action.PLACE_WIND_TURBINE.value,
    pygame.K_u: Action.PLACE_IRRIGATOR.value,
    pygame.K_r: Action.PLACE_PURIFIER.value,
    pygame.K_DOWN: Action.DOWN.value,
    pygame.K_UP: Action.UP.value,
    pygame.K_RIGHT: Action.RIGHT.value,
    pygame.K_LEFT: Action.LEFT.value,
}

EPISODES = 5000

def handle_action(event_key, map_instance):
    """
    Handles key presses for performing actions on the map.
    Returns the updated action type or None if no action is performed.
    """
    action = ACTION_MAPPING.get(event_key)
    if action:
        map_instance.step(action)


def ai_console_mode(env: Env):
    """Runs the AI console mode."""
    agent = AIAgent(env)
    env.set_agent(agent)
    env.step(Action.PLACE_WIND_TURBINE)

    for i in range(EPISODES):
        done = False
        while not done:
            _, _, done = agent.do()
        if agent.has_win():
            win_or_lose = "Win"
        else:
            win_or_lose = "Lose"
        print(f'Episode {agent.qtable.episode}: {win_or_lose}!\tScore: {agent.score}\tEpsilon: {agent.qtable.epsilon}')
        agent.qtable.decrease_epsilon()
        agent.qtable.episode += 1
        agent.qtable.save_qtable()
        env.reset()


def ai_gui_mode(env: Env):
    """Runs the AI GUI mode."""
    agent = AIAgent(env)
    env.set_agent(agent)
    map_instance = EcoEnv(env)

    pygame.key.set_repeat(200, 50)

    for i in range(EPISODES):
        map_instance.render()
        map_instance.grass_animation_count += 1
        map_instance.grass_animation_count %= 210

        done = False
        while not done:
            action, reward, done = agent.do()
            print(f'Action: {action}\tReward: {reward}\tScore: {agent.score}\tPosition: {agent.position}')
            print(agent.qtable)
            # time.sleep(1)
        if agent.has_win():
            win_or_lose = "Win"
        else:
            win_or_lose = "Lose"
        print(f'Episode {agent.qtable.episode}: {win_or_lose}!\tScore: {agent.score}\tEpsilon: {agent.qtable.epsilon}')
        agent.qtable.save_qtable()
        agent.qtable.decrease_epsilon()
        env.reset()
    map_instance.close()


def human_mode(env: Env):
    """Runs the human mode."""
    agent = Agent(env)
    env.set_agent(agent)
    map_instance = EcoEnv(env)

    pygame.key.set_repeat(200, 50)

    done = False
    while not done:
        map_instance.render()
        map_instance.grass_animation_count += 1
        map_instance.grass_animation_count %= 210

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                handle_action(event.key, map_instance)
    map_instance.close()


CURRENT_MODE = Mode.AI_CONSOLE
MODE_MAPPING = {
    Mode.AI_CONSOLE: ai_console_mode,
    Mode.AI_GUI: ai_gui_mode,
    Mode.HUMAN: human_mode,
}

def main():
    """Main function to run the EcoEnv game."""
    env = Env()

    print("MODE:", CURRENT_MODE)
    mode_function = MODE_MAPPING[CURRENT_MODE]
    mode_function(env)


if __name__ == "__main__":
    main()
