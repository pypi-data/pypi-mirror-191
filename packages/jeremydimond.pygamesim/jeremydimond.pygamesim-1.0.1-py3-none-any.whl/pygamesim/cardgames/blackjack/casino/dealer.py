import random

from pygamesim.cardgames.cards import create_deck


class Dealer:
    def __init__(self, number_of_decks: int = 1, shoe_cut_penetration: float = 1.0):
        assert number_of_decks > 0
        self._shoe_cut_penetration = shoe_cut_penetration
        self._shoe = create_deck(number_of_decks=number_of_decks)
        self._shuffle()

    def _shuffle(self):
        random.shuffle(self._shoe)
        self._next_card_index = 0
        self._shuffle_trigger_index = self._shoe_cut_penetration * float(len(self._shoe))

    def prepare_next_hand(self):
        if self._next_card_index > self._shuffle_trigger_index:
            self._shuffle()

    def deal_next_card(self):
        if int(self._next_card_index) >= int(len(self._shoe)):
            self._shuffle()
        next_card = self._shoe[self._next_card_index]
        self._next_card_index += 1
        return next_card
