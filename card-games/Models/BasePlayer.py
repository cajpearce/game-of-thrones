import Models.HandTypes


class BasePlayer(Models.HandTypes.Hand):
    def choose_cards_to_play(self):
        pass


    def make_turn(self,pile,deck):
        pass


    def validate_move(self,cards,pile):
        return self.check_if_valid_selection(cards) and self.check_if_selected_cards_can_play_on_pile(cards,pile)

    def check_if_valid_selection(self, cards):
        cards.sort()

        for i in range(0,len(cards)):
            curr_card = cards[i]
            if i > 0:
                prev_card = cards[i-1]
                if prev_card == curr_card:
                    return False

            if curr_card not in self.cards:
                return False

        return True

    def check_if_selected_cards_can_play_on_pile(self,cards, pile):
        '''

        :param cards: Assume that the order is the order that the player wants to play the cards in
        :param pile: The top card will be used
        :return: return true if it's an acceptable move
        '''

        if not self.can_this_card_be_played_on_pile(cards[0],pile):
            return False

        first_card = cards[0]

        # TODO implement Ace checking
        for i in range(1, len(cards)):
            if not first_card.is_same_value(cards[i]):
                return False

        return True

    def can_this_card_be_played_on_pile(self,card,pile):
        return card.is_same_suit(pile.top_card()) or card.is_same_value(pile.top_card()) or card.value == "A"

    def check_if_can_play_on_pile(self,pile):
        '''
        Used to determine whether the player should just pick up or if he has options
        :param pile: the pile hand
        :return: returns True if the player can play, False if the player cannot play and must pick up
        '''

        top_card = pile.top_card()

        for card in self.cards:
            if self.can_this_card_be_played_on_pile(card, pile):
                return True

        return False