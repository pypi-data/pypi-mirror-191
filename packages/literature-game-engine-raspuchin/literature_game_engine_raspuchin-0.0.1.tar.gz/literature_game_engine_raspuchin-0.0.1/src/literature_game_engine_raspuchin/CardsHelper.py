from .Card import Card
from .Hand import Hand
from typing import Generator
from random import shuffle
from math import floor

# define cards and their suits
suitedCards = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
# joker and suits are defined as First Joker and Second Joker
jokers = "Joker"
jokerSuits = ["First", "Second"]
# number of cards in the deck
NUM_CARDS = 54

# card position to help order the cards in a readable manner
cardPosition = suitedCards + [jokers]


def deal(num_players: int) -> Generator[Hand]:
    """
    Form a shuffled deck and deal it to the number of players in the game
    :param num_players: number of players playing the game
    :return: generator of hands, to be assigned to the player
    """
    deck = []
    for suit in suits:
        for number in suitedCards:
            deck.append(Card(number, suit))

    for suit in jokerSuits:
        deck.append(Card(number, suit))

    shuffle(deck)

    def divide_into_chunk(l, n):
        for i in range(0, len(l), n):
            yield Hand(l[i:i + n])

    return divide_into_chunk(deck, floor(NUM_CARDS / num_players))


def validate_card(number: str, suit: str) -> bool:
    """
    Validate if a card exists
    :param number: number of the card
    :param suit: suit of the card
    :return:
    """
    if (number in suitedCards and suit in suits) or (number == jokers and suit in jokerSuits):
        print('Card correct')
        return True
    print('Card number or suit incorrect')
    return False
