import unittest
from Controllers.Controller import Player
from Models.HandTypes import Deck, Pile
from Models.Card import Card

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.players = [Player(1),Player(2)]
        self.deck = Deck(shuffle_cards=False)
        self.pile = Pile()

        self.deck.deal(self.players, 15)
        self.deck.give_top_card(self.pile)

        self.test_player = Player(3)
        self.test_pile = Pile()
        pile.add_card(Card("A", "H"))

        self.test_player.cards = [
            Card("A", "C"),
            Card("2", "H"),
            Card("3", "H"),
            Card("3", "D"),
            Card("4", "D"),
            Card("4", "D"),
        ]


    def test_7_cards_each(self):
        self.assertEqual(len(self.players[0]), len(self.players[1]))

    def test_1_card_pile(self):
        self.assertEqual(len(self.pile), 1)

    def test_52_cards_total(self):
        self.assertEqual(len(self.pile) + len(self.deck) + len(self.players[0]) + len(self.players[1]), 52)

    def test_pile_card(self):
        print(self.pile.top_card())
        self.assertEqual(self.pile.top_card(),Card("9","D"))

    def play_on_ace(self):
        self.test_player.validate_move(
            [self.test_player.cards[0]]
        )


if __name__ == '__main__':
    unittest.main()
