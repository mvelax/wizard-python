from random import shuffle
from collections import Counter


class Player:

    def __init__(self):
        self.hand = []
        self.score = 0
        self.wins = 0
        self.prediction = -1

    def get_playable_cards(self, first):
        playable_cards = []
        first_colors = []
        if first is None:
            return self.hand
        for card in self.hand:
            # White cards can ALWAYS be played.
            if card.color == "White":
                playable_cards.append(card)
            # First card color can ALWAYS be played.
            elif card.color == first.color:
                first_colors.append(card)
            # Other colors can only be played if there
            # no cards of the first color in the hand.
        if len(first_colors) > 0:
            return playable_cards + first_colors
        else:
            # Cannot follow suit, use ANY card.
            return self.hand

    def play_card(self, trump, first, played):
        raise NotImplementedError("This needs to be implemented by your Player class")

    def get_prediction(self, trump, predictions):
        raise NotImplementedError("This needs to be implemented by your Player class")

    def get_trump_color(self):
        raise NotImplementedError("This needs to be implemented by your Player class")

    def set_score(self, score):
        self.score = score

class RandomPlayer(Player):

    def __init__(self):
        super().__init__()

    def play_card(self, trump, first, played):
        possible_actions = super().get_playable_cards(first)
        if not isinstance(possible_actions, list):
            possible_actions = list(possible_actions)
        shuffle(possible_actions)
        card_to_play = possible_actions[0]
        self.hand.remove(card_to_play)
        # print("Playing card {} from {}".format(card_to_play, self.hand))
        return card_to_play

    def get_prediction(self, trump, predictions):
        return len(self.hand)//len(predictions)

    def get_trump_color(self):
        color_counter = Counter()
        for card in self.hand:
            color = card.color
            if color == "White":
                continue
            color_counter[color] += 1
        return color_counter.most_common(1)[0][0]
