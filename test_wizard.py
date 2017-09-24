from unittest import TestCase
from random import seed


class TestWizard(TestCase):
    def test_play(self):
        from Wizard import Wizard
        seed(2)
        wiz = Wizard(4)
        self.assertIsNotNone(wiz.play())

