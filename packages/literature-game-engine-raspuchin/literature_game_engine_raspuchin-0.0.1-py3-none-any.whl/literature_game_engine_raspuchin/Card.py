"""Number offset and Suit Value are used to calculate the set of a card
   Set number is defined as:
        0 if the card is a 7 or a joker
        Spades 1-2, Clubs 3-4, Hearts 5-6, Diamonds 7-8
        for each of the 2 sets cards A-6 go to the lower one and cards 8-K go to the higher one
"""
numberOffset = {
    "Ace": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": -1,
    "8": 1,
    "9": 1,
    "10": 1,
    "Jack": 1,
    "Queen": 1,
    "King": 1,
    "Joker": -1
}
suitValue = {
    "Spades": 1,
    "Clubs": 3,
    "Hearts": 5,
    "Diamonds": 7,
    "First": -1,
    "Second": -1
}


class Card:
    """
    Class card to represent a card
    Encapsulates the card value, suit and set it belongs to.
    """

    def __init__(self, number: str, suit: str):
        self.number = number
        self.suit = suit
        self.set = self.set_set()

    def set_set(self):
        if self.number == '7' or self.number == 'Joker':
            return 0
        return numberOffset[self.number] + suitValue[self.suit]

    def __str__(self):
        if self.number == 'Joker':
            return f"{self.suit} {self.number}"
        return f"{self.number} of {self.suit}"
