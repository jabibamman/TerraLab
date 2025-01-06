import numpy as np
import random
from terra_lab.envs.agent import Agent
from terra_lab.envs.eco_env import EcoEnv
from terra_lab.utils.enums import MACHINE_TYPE
from terra_lab.utils.enums import MAP_STATES

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.env = env
        self.map_instance = EcoEnv(env)
        self.agent = self.map_instance.agent
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.reward = 0
        self.q_table = self.load_q_table()
        self.actions = ["place_wind_turbine", "place_purifier", "place_irrigator", "move_up", "move_down", "move_left", "move_right"]

    def choose_action(self, state):
        """Choisit une action en utilisant ε-greedy."""
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(range(len(self.actions)))
        else:
            x, y = state
            return np.argmax(self.q_table[x, y, :])

    def save_q_table(self, filename="q_table.npy"):
        """Sauvegarde la Q-table dans un fichier."""
        np.save(filename, self.q_table)

    def load_q_table(self, filename="q_table.npy"):
        """Charge la Q-table depuis un fichier."""
        try:
            return np.load(filename)
        except FileNotFoundError:
            print("Fichier de Q-table introuvable, création d'une nouvelle Q-table.")
            return np.zeros(
            (self.env.grid_size, self.env.grid_size, len(MACHINE_TYPE) + 4))
   
            
    def update_q_table(self, state, action, reward, next_state):
        """Met à jour la Q-table selon la règle de Q-learning."""
        x, y = state
        next_x, next_y = next_state
        best_next_action = np.argmax(self.q_table[next_x, next_y, :])
        td_target = reward + self.discount_factor * self.q_table[next_x, next_y, best_next_action]
        td_error = td_target - self.q_table[x, y, action]
        self.q_table[x, y, action] += self.learning_rate * td_error

    def train(self, episodes=1000, q_table_file="q_table.npy"):
        """Entraîne l'agent sur un certain nombre d'épisodes."""
        
        for episode in range(episodes):
            self.agent.reset()
            self.map_instance.reset()
            self.reward = 0
            state = (self.agent.pos_x, self.agent.pos_y)
            done = False            

            while not done:

                with open("output.txt", "a") as file:
                    print(f"Episode {episode}, Exploration Rate: {self.exploration_rate:.2f}, State: {state}, Done: {done}, Reward: {self.reward}", file=file)

                action_idx = self.choose_action(state)
                action = self.actions[action_idx]
                if action == "move_right" : 
                    self.agent.move_right()
                elif action == "move_left" :
                    self.agent.move_left()
                elif action == "move_up" :
                    self.agent.move_up()
                elif action == "move_down" :
                    self.agent.move_down()
                elif action == "place_wind_turbine" :
                    self.agent.place_wind_turbine()
                elif action == "place_purifier" :
                    self.agent.place_purifier()
                elif action == "place_irrigator" :
                    self.agent.place_irrigator()
                else:
                    print("Erreur : action inconnue")

                next_state = (self.agent.pos_x, self.agent.pos_y)
                self.reward = self.reward + self.compute_reward(next_state)
                self.update_q_table(state, action_idx, self.reward, next_state)

                state = next_state


                self.map_instance.render()

                done = self.check_done()

            self.exploration_rate = max(self.exploration_rate * self.exploration_decay, 0.01)

            self.save_q_table(q_table_file)
  

    def check_done(self):
        """Condition pour signaler la fin d'un épisode (personnalisable)."""
        # Exemple de condition : tous les états fertiles sont remplis
        return self.agent.has_win() or self.agent.has_lose()


    def compute_reward(self, state):
        """Calcule la récompense pour l'état donné."""
        x, y = state
        if self.env.state[x, y] == MAP_STATES.FERTILE_DIRT.value.value:
            return 1
        elif self.env.state[x, y] == MAP_STATES.WIND_TURBINE.value.value:
            return 5
        elif self.agent.has_win():
            return 1000
        elif self.agent.has_lose():
            return -500
        elif self.env.state[x, y] == MAP_STATES.GRASS.value.value:
            return 10
        elif self.env.state[x, y] == MAP_STATES.UNFERTILE_DIRT.value.value:
            return -1
            
        return -1
