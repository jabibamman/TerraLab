import json
import random
import os

from terra_lab.envs.action import Action
from terra_lab.rl.state import State


class QTable:
    def __init__(self, learning_rate=1.0, discount_factor=1.0, epsilon=0.1):
        self.qtable = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.episode = 1
        self.load_qtable()


    def set(self, state, action, reward, new_state):
        if new_state not in self.qtable:
            self.qtable[new_state] = { Action.UP: 0, Action.DOWN: 0, Action.LEFT: 0, Action.RIGHT: 0, Action.PLACE_WIND_TURBINE: 0, Action.PLACE_IRRIGATOR: 0, Action.PLACE_PURIFIER: 0 }
        change = reward + self.discount_factor * max(self.qtable[new_state].values()) - self.qtable[state][action]
        self.qtable[state][action] += self.learning_rate * change


    def best_action(self, state) -> Action:
        if state not in self.qtable:
            self.qtable[state] = { Action.UP: 0, Action.DOWN: 0, Action.LEFT: 0, Action.RIGHT: 0, Action.PLACE_WIND_TURBINE: 0, Action.PLACE_IRRIGATOR: 0, Action.PLACE_PURIFIER: 0 }

        if random.random() < self.epsilon:
            return random.choice(list(Action))

        return max(self.qtable[state], key=self.qtable[state].get)


    def decrease_epsilon(self):
        self.epsilon *= 0.99
        if self.epsilon < 0.1:
            self.epsilon = 0.1


    def save_qtable(self, filename="qtable.json"):
        data = {
            "episode": self.episode,
            "epsilon": self.epsilon,
            "qtable": {
                str(k): {action.name: v for action, v in actions.items()} for k, actions in self.qtable.items()
            }
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_qtable(self, filename="qtable.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)

            self.episode = data.get("episode", 0)
            self.epsilon = data.get("epsilon", 0.1)

            self.qtable = {
                State.from_str(k): {Action[action]: v for action, v in actions.items()}
                for k, actions in data["qtable"].items()
            }

    def __repr__(self):
        res = 'STATE\t\t\t\tUP\t\tDOWN\tLEFT\tRIGHT\tTURB\tIRRIG\tPURIF\n'
        for state in self.qtable:
            res += str(state) + "\t"
            for action in self.qtable[state]:
                res += f'{self.qtable[state][action]:7.1f}\t'
            res += '\n'
        return res
