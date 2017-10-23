from random import shuffle, randrange, choice
from collections import Counter
import Card


class Player(object):

    def __init__(self):
        self.hand = []
        self.score = 0
        self.reward = 0
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

    def play_card(self, trump, first, played, players, played_in_game):
        raise NotImplementedError("This needs to be implemented by your Player class")

    def get_prediction(self, trump, predictions, players):
        raise NotImplementedError("This needs to be implemented by your Player class")

    def get_trump_color(self):
        raise NotImplementedError("This needs to be implemented by your Player class")

    def give_reward(self, reward):
        self.reward = reward
        self.score += reward

    def get_state(self):
        return self.score, self.wins, self.prediction

    def reset_score(self):
        self.score = 0


class RandomPlayer(Player):
    """A completely random agent, it always chooses all
    its actions randomly"""

    def __init__(self):
        super().__init__()

    def play_card(self, trump, first, played, players, played_in_game):
        """Randomly play any VALID card.
        Returns:
            card_to_play: (Card) the chosen card from the player hand.
            """
        possible_actions = super().get_playable_cards(first)
        if not isinstance(possible_actions, list):
            possible_actions = list(possible_actions)
        shuffle(possible_actions)
        card_to_play = possible_actions[0]
        self.hand.remove(card_to_play)
        # print("Playing card {} from {}".format(card_to_play, self.hand))
        return card_to_play

    def get_prediction(self, trump, predictions, players):
        """Randomly return any number of wins between 0 and total number
         of games.
         """
        prediction = randrange(len(self.hand))
        self.prediction = prediction
        return prediction

    def get_trump_color(self):
        # Randomly return any color except white.
        return choice(Card.Card.colors[1:])


class AverageRandomPlayer(RandomPlayer):
    """Agent that uses random cards, but chooses an 'average'
    prediction of wins and a trump color corresponding to
    the color the agent has the most of in its hand."""

    def __init__(self):
        super().__init__()

    def get_prediction(self, trump, predictions, players):
        prediction = len(self.hand) // len(predictions)
        self.prediction = prediction
        return prediction

    def get_trump_color(self):
        # Return the color the agent has the most of in its hand.
        color_counter = Counter()
        for card in self.hand:
            color = card.color
            if color == "White":
                continue
            color_counter[color] += 1
        if not color_counter.most_common(1):
            return super().get_trump_color()
        else:
            return color_counter.most_common(1)[0][0]
