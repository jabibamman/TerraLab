from terra_lab.envs.action import Action


class QTable:
    def __init__(self, learning_rate=1.0, discount_factor=1.0):
        self.qtable = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor


    def set(self, state, action, reward, new_state):
        if new_state not in self.qtable:
            self.qtable[new_state] = { Action.UP: 0, Action.DOWN: 0, Action.LEFT: 0, Action.RIGHT: 0, Action.PLACE_WIND_TURBINE: 0, Action.PLACE_IRRIGATOR: 0, Action.PLACE_PURIFIER: 0 }
        change = reward + self.discount_factor * max(self.qtable[new_state].values()) - self.qtable[state][action]
        self.qtable[state][action] += self.learning_rate * change


    def best_action(self, state):
        if state not in self.qtable:
            self.qtable[state] = { Action.UP: 0, Action.DOWN: 0, Action.LEFT: 0, Action.RIGHT: 0, Action.PLACE_WIND_TURBINE: 0, Action.PLACE_IRRIGATOR: 0, Action.PLACE_PURIFIER: 0 }
        return max(self.qtable[state], key=self.qtable[state].get)


    def __repr__(self):
        res = ' ' * 13
        res += 'U      D      L      R\n'
        for state in self.qtable:
            res += str(state) + " "
            for action in self.qtable[state]:
                res += f'{self.qtable[state][action]:7.1f}'
            res += '\n'
        return res