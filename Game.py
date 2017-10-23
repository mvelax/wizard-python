from Card import Deck, Card
from Trick import Trick


class Game(object):
    """Game object, plays a number of tricks and awards points depending
    on the outcome of the tricks and the predictions."""

    def __init__(self, game_num, players):
        self.game_num = game_num
        self.players = players
        self.deck = Deck()
        self.predictions = [-1]*len(players)
        self.trump_card = None
        # -1 adjusts for 1-index in game numbers and 0-index in players
        self.first_player = (game_num-1) % len(players)
        self.played_cards = []

    def play(self):
        #print("Playing game #{}".format(self.game_num))
        # New game, new deck. No played cards.
        self.played_cards = []
        self.trump_card = self.distribute_cards()[0]
        if self.trump_card is None:
            # We distributed all cards, the trump is N. (No trump)
            self.trump_card = Card("White", 0)
        else:
            self.played_cards.append(self.trump_card)
        if self.trump_card.value == 14:
            # Trump card is a Z, ask the dealer for a trump color.
            self.trump_card.color =\
                self.players[self.first_player].get_trump_color()
        # Now that each player has a hand, ask for predictions.
        self.ask_for_predictions()
        # print("Final predictions {}".format(self.predictions))
        # Reset all wins.
        wins = [0]*len(self.players)
        for i in range(len(self.players)):
            self.players[i].wins = wins[i]
        for trick_num in range(self.game_num):
            # Play a trick for each card in the hand (or game number).
            trick = Trick(self.trump_card, self.players, self.first_player,
                          self.played_cards)
            winner, trick_cards = trick.play()
            # Trick winner gets a win and starts the next trick.
            wins[winner] += 1
            self.first_player = winner
            # Game keeps track of the played cards.
            self.played_cards += trick_cards
            # Update wins
            for i in range(len(self.players)):
                self.players[i].wins = wins[i]
            #print("{} won the game!".format(winner))
        return self.get_scores(wins)

    def distribute_cards(self):
        # Draw as many cards as game num.
        for _ in range(self.game_num):
            for player in self.players:
                player.hand += self.deck.draw()
        # Flip the next card, that is the trump card.
        if self.deck.is_empty():
            return [None]
        else:
            return self.deck.draw()

    def ask_for_predictions(self):
        num_players = len(self.players)
        for i in range(num_players):
            # Start with the first player and ascend, then reset at 0.
            current_player_index = (self.first_player + i) % num_players
            player = self.players[current_player_index]
            prediction = player.get_prediction(self.trump_card,
                                               self.predictions,
                                               self.players)
            self.predictions[current_player_index] = prediction
            """print("Player {} predicted {}".format(current_player_index,
                                                  prediction))"""

    def get_scores(self, wins):
        scores = [0]*len(self.players)
        for i in range(len(self.players)):
            difference = self.predictions[i] - wins[i]
            if difference == 0:
                scores[i] = 20 + wins[i]*10
            else:
                scores[i] = -10*abs(difference)
            self.players[i].give_reward(scores[i])
        return scores
