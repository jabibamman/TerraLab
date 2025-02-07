import numpy as np
import random
from terra_lab.envs.agent import Agent
from terra_lab.envs.eco_env import EcoEnv
from terra_lab.utils.enums import MACHINE_TYPE
from terra_lab.utils.enums import MAP_STATES
import matplotlib.pyplot as plt
from torch.utils.tensorboard import SummaryWriter 
import datetime 

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
        self.env = env
        self.map_instance = EcoEnv(env)
        self.agent = self.map_instance.agent
        self.actions = ["place_wind_turbine", "place_purifier", "place_irrigator", "move_up", "move_down", "move_left", "move_right"]

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.reward = 0
        self.load_q_table()
        self.writer = SummaryWriter(log_dir="runs/grid_40_40" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

    def choose_action(self, state):
        """Choisit une action en utilisant ε-greedy."""
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(range(len(self.actions)))
        else:
            x, y = state
            return np.argmax(self.q_table[x, y, :])

    def save_q_table(self, filename="q_table.npz"):
        np.savez(filename, 
                q_table=self.q_table, 
                exploration_rate=self.exploration_rate)


    def load_q_table(self, filename="q_table.npz"):
        try:
            data = np.load(filename)
            loaded_q_table = data["q_table"]
            if loaded_q_table.shape[0] != self.env.grid_size or loaded_q_table.shape[1] != self.env.grid_size:
                print("Q-table incompatible, réinitialisation à la taille :",
                    (self.env.grid_size, self.env.grid_size))
                self.q_table = np.zeros((self.env.grid_size, self.env.grid_size, len(self.actions)))
                self.exploration_rate = 1.0
            else:
                self.q_table = loaded_q_table
                self.exploration_rate = data["exploration_rate"].item()
        except FileNotFoundError:
            print("Fichier de Q-table introuvable, création d’une nouvelle Q-table.")
            self.q_table = np.zeros((self.env.grid_size, self.env.grid_size, len(self.actions)))
            self.exploration_rate = 1.0

            
    def update_q_table(self, state, action, reward, next_state):
        """Met à jour la Q-table selon la règle de Q-learning."""
        x, y = state
        next_x, next_y = next_state
        best_next_action = np.argmax(self.q_table[next_x, next_y, :])
        td_target = reward + self.discount_factor * self.q_table[next_x, next_y, best_next_action]
        td_error = td_target - self.q_table[x, y, action]
        self.q_table[x, y, action] += self.learning_rate * td_error

    def train(self, episodes=1000, q_table_file="q_table.npz"):
        """Entraîne l'agent sur un certain nombre d'épisodes."""
        if self.q_table.any():
            print("Q-table déjà chargée, entraînement en cours.")
            self.exploration_rate = 0.1
        cumulative_rewards = []

        for episode in range(episodes):
            self.agent.reset()
            self.map_instance.reset()
            self.reward = 0
            total_reward = 0
            state = (self.agent.pos_x, self.agent.pos_y)
            done = False            

            while not done:
                action_idx = self.choose_action(state)
                action = self.actions[action_idx]

                self.agent.last_action = action

                if action == "move_right":
                    self.agent.move_right()
                elif action == "move_left":
                    self.agent.move_left()
                elif action == "move_up":
                    self.agent.move_up()
                elif action == "move_down":
                    self.agent.move_down()
                elif action == "place_wind_turbine":
                    self.agent.place_wind_turbine()
                elif action == "place_purifier":
                    self.agent.place_purifier()
                elif action == "place_irrigator":
                    self.agent.place_irrigator()
                else:
                    print("Erreur : action inconnue")

                next_state = (self.agent.pos_x, self.agent.pos_y)

                immediate_reward = self.compute_reward(next_state)
                self.reward += immediate_reward
                self.update_q_table(state, action_idx, immediate_reward, next_state)

                state = next_state

                #self.map_instance.render()
                done = self.check_done()

            with open("results/output.txt", "a") as file:
                print(f"Episode {episode}, Exploration Rate: {self.exploration_rate:.2f}, Win :{self.agent.has_win()}, Lose :{self.agent.has_lose()} , Reward: {self.reward}", file=file)

            self.exploration_rate = max(self.exploration_rate * self.exploration_decay, 0.01)

            if episode % 1000 == 0:
                self.save_q_table(q_table_file)
                print(f"Q-table sauvegardée à l'épisode {episode}")  
        
            self.writer.add_scalar("TotalReward", self.reward, episode)
            self.writer.flush() 

        self.writer.close()
        
    def check_done(self):
        """Condition pour signaler la fin d'un épisode (personnalisable)."""
        if self.agent.has_win() : 
            print("HasWin : ",self.agent.has_win())
        return self.agent.has_win() or self.agent.has_lose()

    def plot_learning_curve(self, rewards, filename="learning_curve.png"):
        """Trace la courbe d'apprentissage et la sauvegarde en tant qu'image, sans l'afficher."""
        plt.figure(figsize=(10, 6))
        plt.plot(rewards, label="Récompenses cumulées par épisode")
        plt.xlabel("Épisodes")
        plt.ylabel("Récompenses cumulées")
        plt.title("Courbe d'apprentissage de l'agent Q-Learning")
        plt.legend()
        plt.grid(True)
        plt.savefig("results/" + filename) 

    def compute_reward(self, state):
        """Calcule la récompense pour l'état donné."""
        x, y = state

        if self.agent.last_action == "place_wind_turbine":
            if self.env.state[x, y] != MAP_STATES.ROCK.value.value:
                return -1000
            else:
                return 100

        elif self.agent.last_action == "place_irrigator":
            if self.env.state[x, y] != MAP_STATES.FERTILE_DIRT.value.value:
                return -1000
            else:
                return 50

        elif self.agent.last_action == "place_purifier":
            if self.env.state[x, y] != MAP_STATES.UNFERTILE_DIRT.value.value:
                return -1000
            else:
                return 50

        if self.env.state[x, y] == MAP_STATES.GRASS.value.value:
            return 100
        elif self.env.state[x, y] == MAP_STATES.FERTILE_DIRT.value.value:
            return 10
        elif self.env.state[x, y] == MAP_STATES.UNFERTILE_DIRT.value.value:
            return -1
        
        if self.agent.has_win():
            return 1000
        elif self.agent.has_lose():
            return -500

        return -1

