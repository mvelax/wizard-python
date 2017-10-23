from unittest import TestCase
from random import seed
from Player import RandomPlayer, AverageRandomPlayer
from RLAgents import RLAgent
import plotting
import numpy as np


class TestWizard(TestCase):
    def test_play(self):
        from Wizard import Wizard
        seed(2)
        wiz = Wizard(4)
        self.assertIsNotNone(wiz.play())

    def test_play_with_RLAgent(self):
        from Wizard import Wizard
        seed(2)
        players = [RandomPlayer() for _ in range(5)]
        players.append(RLAgent())
        wiz = Wizard(players=players)
        self.assertIsNotNone(wiz.play())

    def test_1000_play_with_RL(self):
        from Wizard import Wizard
        seed(2)
        games = 1000
        players = [AverageRandomPlayer() for _ in range(5)]
        players.append(RLAgent())
        players[-1].load_estimator()
        scores = []
        for i in range(games):
            if i % 100 == 0:
                print("{}/{}".format(i, games))
            wiz = Wizard(players=players)
            scores.append(wiz.play())
        players[-1].save_estimator()
        scores = np.array(scores)
        plotting.plot_moving_average_scores(scores, 100)
