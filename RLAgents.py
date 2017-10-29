import Estimators
import Policies
import Featurizers
from Player import Player, RandomPlayer, AverageRandomPlayer
import numpy as np


class RLAgent(AverageRandomPlayer):
    """A computer player that learns using reinforcement learning."""

    def __init__(self, estimator=None, policy=None, featurizer=None):
        super().__init__()
        if estimator is None:
            self.estimator = Estimators.DQNEstimator()
        else:
            self.estimator = estimator
        if policy is None:
            self.policy = Policies.EGreedyPolicy(self.estimator, epsilon=0.1)
        else:
            self.policy = policy
        if featurizer is None:
            self.featurizer = Featurizers.Featurizer()
        else:
            self.featurizer = featurizer
        self.old_state = None
        self.old_score = 0
        self.old_action = None

    def play_card(self, trump, first, played, players, played_in_game):
        """Plays a card according to the estimator Q function and learns
        on-line.
        Relies on scores being updated by the environment to calculate reward.
        Args:
            trump: (Card) trump card.
            first: (Card) first card.
            played: (list(Card)) list of cards played in Trick, may be empty.
            players: (list(Player)) list of players in the game, including this
            player.
            played_in_game: (list(Card)) list of cards played so far in the
            game, may be empty.

        Returns:
            card_to_play: (Card) the card object that the player
             decided to play.
        """
        state = self.featurizer.transform(self, trump, first, played, players,
                                          played_in_game)
        terminal = False
        if self.old_state is not None and self.old_action is not None:
            r = self.reward
            if r != 0:
                terminal = True
                # If we got a reward, it's a terminal state.
                # We signal this with an s_prime == None
                self.estimator.update(self.old_state, self.old_action, r, None)
            else:
                self.estimator.update(self.old_state, self.old_action, r, state)

        probs = self.policy.get_probabilities(state)
        a = np.random.choice(len(probs), p=probs)
        card_to_play = self._remove_card_played(a)
        self.old_state = None if terminal else state
        self.old_action = a
        self.give_reward(0)  # After playing a card, the reward is 0.
        # Unless it's the last card of the game, then the Game object will
        # call give_reward before the next play_card, setting the correct reward
        return card_to_play

    def save_estimator(self, name="default"):
        self.estimator.save(name)

    def load_estimator(self, name="default"):
        self.estimator.load(name)

    def _remove_card_played(self, a):
        """
        Given an action (integer) remove a card equivalent to it from the
        player's hand and return it.

        Args:
            a: (int) The action taken. Remove a card with the same code.
            If there is more than one that matches, it does not matter which,
            but just remove one.

        Returns:
            card_to_play: The card corresponding to the action.

        Raises:
            RuntimeError when the action does not correspond to any card.

        """
        assert isinstance(a, int), "action played is not an int as expected"
        card_to_return = None
        for card in self.hand:
            if int(card) == a:
                card_to_return = card
                self.hand.remove(card)
                break
        if card_to_return is None:
            raise RuntimeError("Computer did not find a valid card for this"
                               "action.\nHand: {}\nAction: {}".format(self.hand,
                                                                      a))
        return card_to_return
