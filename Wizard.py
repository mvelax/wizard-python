class Wizard:
    """
    This class contains all the game.
    Create a Wizard instance with the number of players and run play.
    """
    NUM_CARDS = 60

    def __init__(self, num_players):
        self.num_players = num_players
        self.scores = [0]*num_players
        self.games_to_play = Wizard.NUM_CARDS//num_players
        self.players = []
        for player in num_players:
            # Initialize all players
            players.append(Player())

    def play(self):
        for game_num in range(1, self.games_to_play+1):
            game = Game(game_num, players)
            score = game.play()
            for i in range(num_players):
                self.scores[i] += score[i]
        print("Final scores: {}".format(self.scores))
