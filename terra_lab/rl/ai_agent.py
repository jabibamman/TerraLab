from terra_lab.envs.agent import Agent
from terra_lab.rl.qtable import QTable


class AIAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.qtable = QTable()
        self.score = None
        self.history = []


    def reset(self):
        super().reset()
        if self.score is not None:
            self.history.append(self.score)
        self.score = 0


    def do(self):
        # action = choice(list(Action))
        action = self.qtable.best_action(self.position)

        new_position, reward = self.env.do(self.position, action)
        self.qtable.set(self.position, action, reward.value, new_position)
        self.score += reward.value
        self.position = new_position
        return action, reward
