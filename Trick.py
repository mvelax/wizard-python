class Card(object):
    pass


class Trick:
    def __init__(self, trump_card, players, first_player, played_cards):
        self.trump_card = trump_card
        self.players = players
        self.first_player = first_player
        self.first_card = None
        self.played_cards = played_cards

    def play(self):
        winner = None
        num_players = len(self.players)
        played_cards = set()
        for i in range(num_players):
            # Start with the first player and ascend, then reset at 0.
            player = self.players[(self.first_player+i) % num_players]
            played_card = player.play_card(self.trump_card, self.played_cards, self.first_card)
            played_cards.add(played_card)
            if self.first_card is None and played_card != Card("White", 0):
                self.first_card = played_card
            if winner is None or winner[0] < played_card:
                winner = (played_card, player)
        return winner[1], played_cards
