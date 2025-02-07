from collections import deque

from terra_lab.envs.action import MOVES
from terra_lab.envs.agent import Agent
from terra_lab.rl.qtable import QTable
from terra_lab.rl.state import State, Radar
from terra_lab.utils.enums import MAP_STATES


class AIAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.qtable = QTable()
        self.state = None
        self.score = None # TODO
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


    def find_nearest_element(self, element: MAP_STATES):
        queue = deque([(self.position, 0)])
        visited = { self.position }

        while queue:
            pos, dist = queue.popleft()

            if self.env.state[pos.to_tuple()] == element.value.value:
                next_rock = Radar(self.position.y > pos.y, self.position.y < pos.y, self.position.x < pos.x, self.position.x > pos.x)
                return next_rock, dist

            for direction in MOVES:
                new_pos = pos + MOVES[direction]
                if 0 <= new_pos.x < self.env.grid_size and 0 <= new_pos.y < self.env.grid_size and new_pos not in visited:
                    queue.append((new_pos, dist + 1))
                    visited.add(new_pos)

        return None, -1


    def get_current_state(self) -> State:
        next_rock, distance_next_rock = self.find_nearest_element(MAP_STATES.ROCK)
        next_wind_turbine, distance_next_wind_turbine = self.find_nearest_element(MAP_STATES.WIND_TURBINE)
        bloc_type = self.env.state[self.position.to_tuple()]
        return State(next_rock, next_wind_turbine, distance_next_wind_turbine, bloc_type)
