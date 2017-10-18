from Card import Card, is_new_winner


class Trick(object):
    def __init__(self, trump_card, players, first_player, played_cards_in_game):
        self.trump_card = trump_card
        self.players = players
        self.first_player = first_player
        self.first_card = None
        self.played_cards_in_game = played_cards_in_game

    def play(self):
        winner = None
        num_players = len(self.players)
        trick_cards = []
        for i in range(num_players):
            player_index = (self.first_player+i) % num_players
            # Start with the first player and ascend, then reset at 0.
            player = self.players[player_index]
            played_card = player.play_card(self.trump_card, self.first_card,
                                           trick_cards, self.players,
                                           self.played_cards_in_game)
            trick_cards.append(played_card)
            if self.first_card is None and played_card.value != 0:
                self.first_card = played_card
            if winner is None or is_new_winner(played_card, winner[0],
                                               self.trump_card,
                                               self.first_card):
                winner = (played_card, player_index)
            """print("First card: {}\nTrump card: {}\nWinning: {}".format(self.first_card,
                                                                       self.trump_card,
                                                                       winner))"""
        return winner[1], trick_cards
