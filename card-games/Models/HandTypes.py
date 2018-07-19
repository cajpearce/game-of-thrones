from Models.Card import Card


class Hand:
     
    def __init__(self):
        self.cards = []

    def __str__(self):
        retter = ""

        for i in range(0,len(self.cards)):
            card = self.cards[i]
            retter += str(card)
            if i < len(self.cards) - 1:
                retter += ", "

        return retter

    def __len__(self):
            return len(self.cards)


    def top_card(self):
        return self.cards[len(self.cards) - 1]

    
    def add_card(self, card):
        if type(card) is Card:
            self.cards.append(card)

    def remove_card(self, card):
        return self.cards.pop(self.cards.index(card))

    def give_card(self, other, card):
        other.add_card(self.remove_card(card))

    def give_nth_card(self, other, n):
        if n >= len(self.cards):
            raise Exception("You have chosen an n too big.")
        
        other.add_card(self.remove_card(self.cards[n]))
  
    def give_top_card(self, other):
        self.give_card(other, self.top_card())

    def give_cards(self, other, cards):
        for card in cards:
            self.give_card(other, card)

    def give_cards_to_pile(self, pile, cards):
        first_card = cards[0]

        if first_card.value == "A" and len(cards):
            raise Exception("Can only play one Ace.")
        
        for card in cards:
            if not card.is_same_value(first_card):
                raise Exception("You have selected cards with differing values")

        same_suit = first_card.is_same_suit(pile.top_card())
        same_value = first_card.is_same_value(pile.top_card())

        if not (same_value and not same_suit or same_suit and not same_value):
            raise Exception("You have not chosen a valid first card.")
        else:
            self.give_cards(pile, cards)

        
    def sort(self):
        self.cards.sort()


    def secret_format(self):
        if len(self) == 1:
            return "There is 1 card."
        else:
            return "There are " + str(len(self)) + " cards."

    
class Deck(Hand):
    def __init__(self, shuffle_cards=True):
        super().__init__()
        self.build_deck()

        if shuffle_cards:
            self.shuffle()
        
    def shuffle(self):
        from random import shuffle
        shuffle(self.cards)
        
    def build_deck(self):
        for suit in Card.SUITS:
            for val in Card.VALUES:
                self.add_card(Card(val, suit))

    def deal(self, hands, number_of_cards = 7):
        for i in range(0,number_of_cards):
            for hand in hands:
                self.give_top_card(hand)

    def __str__(self):
        return self.secret_format()
    
class Pile(Hand):
    def __str__(self):
        return self.secret_format() + " The top card is " + str(self.top_card())
     


