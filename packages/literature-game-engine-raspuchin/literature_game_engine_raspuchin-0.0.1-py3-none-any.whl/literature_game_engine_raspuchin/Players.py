from .Hand import Hand


class Player:
    """
    A player in the game, abstract class to implement common functionality.
    If a new interface for the player is to be created then use this base class to access the data and override the
    play function.
    """
    def __init__(self, name: str, game):
        self.name = name
        self.game = game
        self.hand = None

    def set_hand(self, hand: Hand):
        """
        Set a new hand
        :param hand: hand from the game
        :return: nothing
        """
        self.hand = hand

    def check(self, number: str, suit: str):
        """
        Check if the player has a card and give it in case they do
        :param number: number of the card
        :param suit: suit of the card
        :return: card if found else None
        """
        return self.hand.find_and_remove_card(number, suit) if self.hand is not None else None

    def complete_set(self):  # ToDo
        pass

    def play(self) -> bool:
        # Does nothing. Override in subclasses.
        return False

    def __str__(self):
        return f"----\nPlayer Name: {self.name}\nPlayer Team: {self.team}\nHand: {self.hand}"


class HumanPlayer(Player):
    """
    Human player on CLI
    """
    def __init__(self, name: str, game):
        super().__init__(name, game)

    def play(self) -> bool:
        print(f"{self.name}'s turn:")
        valid = False
        player_name, number, suit = '', '', ''

        while not valid:
            player_name = input('Enter opponents name you want to take a card from: ')
            number = input('Enter number of the card: ')
            suit = input('Enter suit of the card: ')
            valid = self.game.verify_query(player_name, number, suit)

        print('Parameters valid')
        card = self.game.ask_player(player_name, number, suit)
        if card is not None:
            self.hand.add_card(card)
            print('Got the card')
            return True

        print('Did not get the card')
        return False


class ComputerPlayer(Player):
    def __init__(self, name: str, game):
        super().__init__(name, game)

    def play(self) -> bool:
        print("AI Turn")
        return False
