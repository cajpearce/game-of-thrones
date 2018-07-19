class Card:
    SUITS = ("H","D","C","S")
    VALUES = ("A","2","3","4","5","6","7","8","9","10","J","Q","K")

    def __init__(self, value, suit):
        if suit not in Card.SUITS:
            raise Exception("You have provided an invalid suit.")

        if value not in Card.VALUES:
            raise Exception("You have provided an invalid value.")  
        self.suit = suit
        self.value = value

    def __str__(self):
        return self.value + self.suit

    def __lt__(self, other):
        return self.get_hash() < other.get_hash()

    def __eq__(self, other):
        return self.is_same_value(other) and self.is_same_suit(other)
    
    def get_hash(self, pairs = False):
        if pairs:
            return Card.VALUES.index(self.value)*len(Card.SUITS) + Card.SUITS.index(self.suit)        
        return Card.SUITS.index(self.suit)*len(Card.VALUES) + Card.VALUES.index(self.value)
        
    
    def is_same_value(self,other):
        return self.value == other.value

    def is_same_suit(self,other):
        return self.suit == other.suit


