from Models.BasePlayer import BasePlayer
from Models.Card import Card
from Models.HandTypes import Pile, Deck


class Player(BasePlayer):
    # TODO Split this class up into a 'base' class and a class which takes user input

    def __init__(self,name):
        super().__init__()
        self.name = name


    def make_turn(self,pile,deck):
        self.sort()
        self.print_current_board(pile)

        if not self.check_if_can_play_on_pile(pile):
            print("You must pick up.")
            deck.give_top_card(self)
        else:
            chosen_cards = self.choose_cards_to_play()
            while not self.validate_move(chosen_cards,pile):
                # TODO implement giving the cards to the pile
                # TODO implement telling the board that you've "played" these cards

                self.print_current_board(pile)
                chosen_cards = self.choose_cards_to_play()

            self.give_cards_to_pile(pile,chosen_cards)



    def print_current_board(self,pile):
        print("It is your turn, " + str(self.name))
        print("You must play on: " + str(pile.top_card()))
        print("Your current cards: " + str(self))

    # this is meant to override
    def choose_cards_to_play(self):
        '''

        :return: the cards chosen
        '''

        print("Choose your cards (in order): ")
        selection = input()
        return self.parse_from_string_to_cards(selection)


    def parse_from_string_to_cards(self, selection):
        selection.replace(" ","")
        selections = selection.split(",")

        cards = []
        for card in selections:
            cards.append(self.parse_card(card))

        return cards

    def parse_card(self, solid_string):
        val = solid_string[0:(len(solid_string) - 1)]
        suit = solid_string[len(solid_string) - 1]

        return Card(val, suit)


class GameStart:
    def __init__(self, number_of_players):
        self.players = [Player("Player " + str(i+1)) for i in range(0,number_of_players)]
        self.deck = Deck()
        self.pile = Pile()

        self.deck.deal(self.players)
        self.deck.give_top_card(self.pile)

        self.start_loop()

    def start_loop(self):
        while(True):
            for player in self.players:
                player.make_turn(self.pile, self.deck)



if __name__ == '__main__':
    game = GameStart(4)
