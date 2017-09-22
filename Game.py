from Trick import Trick


class Game:

    def __init__(self, game_num, players):
        self.game_num = game_num
        self.players = players
        self.deck = Deck()
        self.predictions = []
        self.trump_card = None
        self.first_player = game_num % len(players)

    def play(self):
        self.trump_card = self.distribute_cards()
        self.ask_for_predictions()
        wins = [0]*len(self.players)
        for trick_num in range(self.game_num):
            trick = Trick(self.trump_card, self.players, self.first_player)
            winner, played_cards = trick.play()
            wins[winner] += 1
            self.first_player = winner

    def distribute_cards(self):
        # Draw as many cards as game num.
        for _ in range(self.game_num):
            for player in self.players:
                player.hand.append(self.deck.draw())
        # Flip the next card, that is the trump card.
        if self.deck.is_empty():
            return None
        else:
            return self.deck.draw()