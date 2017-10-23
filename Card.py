from random import shuffle


class Card(object):

    colors = ("White", "Green", "Red", "Blue", "Yellow")
    DIFFERENT_CARDS = 54

    def __init__(self, color, value):
        if color not in Card.colors or value > 14 or value < 0:
            raise ValueError
        if color == "White" and value not in (0, 14):
            raise ValueError
        if color in Card.colors[1:] and value in (0, 14):
            raise ValueError
        self.color = color
        self.value = value

    def __str__(self):
        return "{} {}".format(self.color, self.value)

    def __repr__(self):
        return str(self)

    def __int__(self):
        # Used for feature vector translation.
        if self.color == "White":
            if self.value == 0:
                # N is 52
                return 52
            else:
                # Z is 53
                return 53
        # The rest is between 0-51 inclusive.
        return (Card.colors.index(self.color)-1)*13 + (self.value - 1)

    @staticmethod
    def int_to_card(x):
        if x == 52:
            return Card("White", 0)
        elif x == 53:
            return Card("White", 14)
        else:
            color = Card.colors[x//13 + 1]
            value = x % 13 + 1
            return Card(color, value)


class Deck(object):

    def __init__(self):
        self.cards = []
        # Add four colors with 1-13 cards.
        for val in range(1, 14):
            for color in Card.colors[1:]:
                self.cards.append(Card(color, val))
        # Add four Zs (white, 14) and four Ns (white, 0)
        for _ in range(4):
            self.cards.append(Card("White", 0))
            self.cards.append(Card("White", 14))
        shuffle(self.cards)

    def draw(self, num=1):
        """
        Returns a list of the drawn cards from the deck.
        Removes the card from the deck.
        :param num: int Number of cards to draw.
        :return: list: Cards drawn
        """
        drawn = []
        for _ in range(num):
            drawn.append(self.cards.pop())
        return drawn

    def is_empty(self):
        return len(self.cards) <= 0


def is_new_winner(new_card, old_card, trump, first_card):
    """
    Returns True if the new_card wins, taking into account trump
    colors, first_card color and order.

    :param new_card: Card played LATER.
    :param old_card: Current winning Card.
    :param trump: Trump card.
    :param first_card: First card played. May be None.
    :return: The winning card.
    """
    # If a Z was played first, it wins.
    if old_card.value == 14:
        return False
    # If not and the new card is a Z, the new card wins.
    if new_card.value == 14:
        return True
    # First N wins, so if the second card is N, it always wins.
    if new_card.value == 0:
        return False
    # Second N wins only if new_card is NOT N.
    elif old_card.value == 0:
        return True
    # If they are both colored cards, the trump color wins.
    if old_card.color == trump.color:
        if new_card.color != trump.color:
            return False
        else: # If both are trump color, the higher value wins.
            return old_card.value < new_card.value
    else:
        # old_card is not trump color, then if new_card is, new_card wins
        if new_card.color == trump.color:
            return True
        else:
            # Neither are trump color, so check for first color.
            if old_card.color == first_card.color:
                if new_card.color != first_card.color:
                    # old card is first_card color but new card is not, old wins.
                    return False
                else:
                    # Both are first_card color, bigger value wins.
                    return old_card.value < new_card.value
