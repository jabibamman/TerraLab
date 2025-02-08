from collections import deque

from terra_lab.envs.action import MOVES, Action
from terra_lab.envs.agent import Agent
from terra_lab.rl.qtable import QTable
from terra_lab.rl.state import State, Radar
from terra_lab.utils.enums import MAP_STATES


class AIAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.qtable = QTable(0.8, 0.9, 1.0)
        self.state = self.get_current_state()
        self.score = 0
        self.history = []


    def reset(self):
        super().reset()
        self.history.append(self.score)
        self.score = 0


    def do(self) -> tuple[Action, int, bool]:
        action = self.qtable.best_action(self.state)

        reward, done = self.env.step(action)
        new_state = self.get_current_state()

        self.qtable.set(self.state, action, reward, new_state)
        self.score += reward
        self.state = new_state
        return action, reward, done


    def find_nearest_element(self, element: MAP_STATES) -> tuple[Radar, int]:
        if self.env.state[self.position.to_tuple()] == element.value.value:
            return Radar(True, True, True, True), 0

        queue = deque([(self.position, 0)])
        visited = { self.position }

        while queue:
            pos, dist = queue.popleft()

            if self.env.state[pos.to_tuple()] == element.value.value:
                next_rock = Radar(self.position.y >= pos.y, self.position.y <= pos.y, self.position.x <= pos.x, self.position.x >= pos.x)
                return next_rock, dist

            for direction in MOVES.values():
                new_pos = pos + direction
                new_pos.x = new_pos.x % self.env.grid_size
                new_pos.y = new_pos.y % self.env.grid_size
                if new_pos not in visited:
                    queue.append((new_pos, dist + 1))
                    visited.add(new_pos)

        return Radar(False, False, False, False), -1


    def get_current_state(self) -> State:
        next_rock, _ = self.find_nearest_element(MAP_STATES.ROCK)
        next_wind_turbine, distance_wind_turbine = self.find_nearest_element(MAP_STATES.WIND_TURBINE)
        bloc_type = int(self.env.state[self.position.to_tuple()])
        return State(next_rock, next_wind_turbine, distance_wind_turbine, bloc_type)
