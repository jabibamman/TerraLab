import json
import os
from json import JSONDecodeError

import matplotlib.pyplot as plt

class ScorePlotter(object):
    def __init__(self, current_score = None):
        self.scores = [current_score] if current_score is not None else []

    def add_score(self, score):
        self.scores.append(score)

    def save_scores(self, filename='scores.json'):
        saved_scores = ScorePlotter.load_scores(filename)
        saved_scores.extend(self.scores)

        with open(filename, 'w') as f:
            f.write(json.dumps({'scores': saved_scores}))

    @classmethod
    def load_scores(cls, filename='scores.json'):
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write("{'scores': []}")

        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except JSONDecodeError:
                data = {'scores': []}

        return data.get('scores')

    def get_saved_and_current_scores(self):
        saved_scores = ScorePlotter.load_scores()

        return saved_scores + self.scores

    def plot_scores(self):
        scores = self.load_scores()

        plt.plot(scores)
        plt.show()