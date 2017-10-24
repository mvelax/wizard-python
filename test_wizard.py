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

    """
    def test_1000_play_with_RL(self):
        from Wizard import Wizard
        # seed(2)
        games = 5000
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
        plotting.plot_moving_average_scores(scores, 500)
    """

    def test_several_RL_one_estimator(self):
        from Wizard import Wizard
        games = 20000
        players = [RLAgent()]
        players[0].load_estimator()
        for rl_player in range(3):
            players.append(RLAgent(estimator=players[0].estimator))
        players.append(AverageRandomPlayer())
        players.append(RandomPlayer())
        scores = []
        for i in range(games):
            if i % 100 == 0:
                print("{}/{}".format(i, games))
            wiz = Wizard(players=players)
            scores.append(wiz.play())
        players[0].save_estimator()
        scores = np.array(scores)
        plotting.plot_moving_average_scores(scores, 100)
