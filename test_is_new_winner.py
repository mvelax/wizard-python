from unittest import TestCase


class TestIs_new_winner(TestCase):
    def test_double_Z(self):
        from Card import Card, is_new_winner
        old = Card("White", 14)
        new = Card("White", 14)
        trump = Card("White", 0)
        first = Card("White", 0)
        self.assertFalse(is_new_winner(new, old, trump, first))

    def test_double_N(self):
        from Card import Card, is_new_winner
        old = Card("White", 0)
        new = Card("White", 0)
        trump = Card("White", 0)
        first = Card("White", 0)
        self.assertFalse(is_new_winner(new, old, trump, first))

    def test_Z_win_trump(self):
        from Card import Card, is_new_winner
        old = Card("White", 14)
        new = Card("Red", 13)
        trump = Card("Red", 1)
        first = Card("Red", 2)
        self.assertFalse(is_new_winner(new, old, trump, first))
        self.assertTrue(is_new_winner(old, new, trump, first))

    def test_bigger_trump_wins(self):
        from Card import Card, is_new_winner
        old = Card("Red", 13)
        new = Card("Red", 12)
        trump = Card("Red", 1)
        first = Card("Red", 2)
        self.assertFalse(is_new_winner(new, old, trump, first))
        self.assertTrue(is_new_winner(old, new, trump, first))

    def test_first_color_wins(self):
        from Card import Card, is_new_winner
        old = Card("Red", 13)
        new = Card("Red", 12)
        invalid = Card("Green", 13)
        trump = Card("White", 0)
        first = Card("Red", 2)
        self.assertFalse(is_new_winner(new, old, trump, first))
        self.assertTrue(is_new_winner(old, new, trump, first))
        self.assertFalse(is_new_winner(invalid, old, trump, first))
