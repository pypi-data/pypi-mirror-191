from .Card import Card
from typing import List
from .CardsHelper import cardPosition


class Hand:
    """
    Class that represents a set of cards in the hand.
    """
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def get_playable_sets(self):
        """
        ToDo shift this function to ComputerPlayer as they are the only ones who need this
        Return the sets the player can use
        :return: sets for which the user can ask cards for or make sets
        """
        playable_sets = set()
        for card in self.cards:
            playable_sets.add(card.set)
        return playable_sets

    def sort(self):
        """
        Sort the cards according to their sets and numbers
        :return: None
        """
        self.cards = sorted(self.cards, key=lambda card: (card.set,
                                                          cardPosition.index(card.number)))

    def add_card(self, card: Card):
        """
        Add a card to the hand
        :param card: card gotten from another player
        :return:
        """
        self.cards.append(card)

    def find_and_remove_card(self, number: str, suit: str):
        """
        Find a card and remove it if it exists, return None if it doesn't exist
        :param number: number of the card
        :param suit: suit of the card
        :return: card if found else None
        """
        index = 0
        while index < len(self.cards):
            if self.cards[index].number == number and self.cards[index].suit == suit:
                return self.cards.pop(index)
            index += 1

        return None

    def __str__(self):
        res = ''
        for card in self.cards:
            res = res + str(card) + '\n'
        return res

    def __len__(self):
        self.sort()
        return len(self.cards)
