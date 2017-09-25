from Game import Game
from Player import RandomPlayer
from random import seed, getstate


class Wizard(object):
    """

    """
    NUM_CARDS = 60

    def __init__(self, num_players):
        self.num_players = num_players
        self.scores = [0]*num_players
        self.games_to_play = Wizard.NUM_CARDS//num_players
        self.players = []
        for player in range(num_players):
            # Initialize all players
            # print("Creating players.")
            self.players.append(RandomPlayer())

    def play(self):
        """
        Starts a game with the generated players.

        Returns:
            list: The scores for each player.

        """
        # print("Playing a Wizard game!")
        for game_num in range(1, self.games_to_play+1):
            game = Game(game_num, self.players)
            score = game.play()
            for i in range(self.num_players):
                self.scores[i] += score[i]
            # print("Scores: {}".format(self.scores))
        # print("Final scores: {}".format(self.scores))
        return self.scores


if __name__ == "__main__":
    print("Playing a random game of 4 players.")
    seed(2)
    wiz = Wizard(4)
    print(getstate())
    print(wiz.play())