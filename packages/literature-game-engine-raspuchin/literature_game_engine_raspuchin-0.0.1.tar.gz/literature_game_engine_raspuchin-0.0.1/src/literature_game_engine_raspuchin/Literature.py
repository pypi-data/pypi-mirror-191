from .Card import Card
from .Hand import Hand
from .CardsHelper import *
from .Players import *
from typing import List

MINIMUM_PLAYERS = 4
MAX_PLAYERS = 8
MAX_ROUNDS = 10


class Literature:
    """
    Class that can create and run the game.
    """
    def __init__(self, playerNames: List[str], playerType=HumanPlayer, alternateType=ComputerPlayer):
        self.playerNames = playerNames
        self.players = []
        self.teamScores = [0, 0]
        self.currentTurn = 0
        self.playerType = playerType
        self.alternateType = alternateType
        self.set_game()

        self.valid_preconditions = False

    def set_game(self):
        """
        The number of players sent in are created as playerType, the rest are created as alternateType.
        Minimum 4 players in the game, 6 and 8 are also accepted.
        :return:
        """
        self.players = []

        num_players = max(len(self.playerNames), MINIMUM_PLAYERS)
        if num_players > MAX_PLAYERS:
            print("Too many players to run correctly (MAX: 8)")
            return

        i = 0
        print(f"Creating {len(self.playerNames)} normal players")
        while i < len(self.playerNames):
            self.players.append(self.playerType(self.playerNames[i], self))
            i += 1
        print(f"Creating {num_players - i} alternate players")
        while i < num_players:
            self.playerNames.append(f"alt{i}")
            self.players.append(self.alternateType(self.playerNames[i], self))
            i += 1

        hands = deal(len(self.players))
        for player, hand in zip(self.players, hands):
            player.set_hand(hand)

        self.valid_preconditions = True

    def play_turn(self):
        """
        If the current player has a hand then they can play. If they get a card or complete a set they can play again.
        Otherwise, the next person gets the turn.
        :return:
        """
        # skip if player has no cards to play
        if len(self.players[self.currentTurn].hand) == 0:
            self.currentTurn = (self.currentTurn + 1) % len(self.players)
            return

        # if turn succeeds then player can play again, else go to next player
        turn_succeeded = self.players[self.currentTurn].play()
        if not turn_succeeded:
            self.currentTurn = (self.currentTurn + 1) % len(self.players)
            print('Turn changes')

    def start_game(self):
        """
        Check if preconditions have been met and play the game
        :return:
        """
        if not self.valid_preconditions:
            print('Pre conditions not met, manually run set_game to see error message in case you missed it.')
            return

        i = 0
        while i < MAX_ROUNDS:
            self.play_turn()
            self.get_one()  # ToDo : Delete
            i += 1

    def verify_query(self, player_name: str, number: str, suit: str):
        """
        Verify if the input is corresponding, useful in cases where input is typed instead of selected
        :param player_name: name of the player
        :param number: number of the card
        :param suit: number of the suit
        :return:
        """
        res = validate_card(number, suit)

        try:
            player_index = self.playerNames.index(player_name)
            print(f"Player name found at index {player_index}")
        except ValueError as e:
            res = False
            print("Player Name not in list of players")

        if res and player_index % 2 == self.currentTurn % 2:
            res = False
            print("That's your teammate :/")

        return res

    def ask_player(self, player_name: str, number: str, suit: str):
        """
        To be used by a player to ask another player, ideally after query has been verified
        :param player_name: name of player
        :param number: number of the card
        :param suit: suit of the card
        :return:
        """
        player_index = self.playerNames.index(player_name)
        return self.players[player_index].check(number, suit)

    def get_one(self):
        # ToDo : Delete
        print(f"{self.players[0]}")

    def __str__(self):
        print(vars(self))
        return '\n'.join([str(player) for player in self.players])
