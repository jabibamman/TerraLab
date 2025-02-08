import sys
import time

import pygame

from terra_lab.envs import EcoEnv
from terra_lab.envs.action import Action
from terra_lab.envs.agent import Agent
from terra_lab.envs.env import Env
from terra_lab.mode import Mode
from terra_lab.rl.ai_agent import AIAgent



ACTION_MAPPING = {
    pygame.K_p: Action.PLACE_WIND_TURBINE,
    pygame.K_u: Action.PLACE_IRRIGATOR,
    pygame.K_r: Action.PLACE_PURIFIER,
    pygame.K_DOWN: Action.DOWN,
    pygame.K_UP: Action.UP,
    pygame.K_RIGHT: Action.RIGHT,
    pygame.K_LEFT: Action.LEFT,
}

EPISODES = 5000

def handle_action(event_key, map_instance):
    """
    Handles key presses for performing actions on the map.
    Returns the updated action type or None if no action is performed.
    """
    action = ACTION_MAPPING.get(event_key)
    if action is not None:
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
            # print(agent.qtable)
            map_instance.render()
            time.sleep(0.3)
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

def plot_mode(env):
    env.score_plotter.plot_scores()

CURRENT_MODE = Mode.AI_CONSOLE
MODE_MAPPING = {
    Mode.AI_CONSOLE: ai_console_mode,
    Mode.AI_GUI: ai_gui_mode,
    Mode.HUMAN: human_mode,
    Mode.PLOT: plot_mode,
}

def choose_mode(mode):
    global CURRENT_MODE
    options_to_mode = {
        '--aic': Mode.AI_CONSOLE,
        '--aig': Mode.AI_GUI,
        '--hc': Mode.HUMAN,
        '--plt': Mode.PLOT,
    }
    CURRENT_MODE = options_to_mode[mode]


def main():
    """Main function to run the EcoEnv game."""
    env = Env()

    if len(sys.argv) > 1:
        choose_mode(sys.argv[1])

    print("MODE:", CURRENT_MODE)
    mode_function = MODE_MAPPING[CURRENT_MODE]
    mode_function(env)


if __name__ == "__main__":
    main()
