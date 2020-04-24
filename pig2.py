import random
import argparse
import time
random.seed(0)


# if the dice rolls one
class ExceptionforOne(Exception):
    pass


# dice class
class Die:
    """Class for the die"""

    def __init__(self):
        self.value = random.randint(1, 6)

    def roll(self):
        """Returns value of rolled dice or exception"""
        self.value = random.randint(1, 6)
        if self.value == 1:
            raise ExceptionforOne

        return self.value

    def __str__(self):
        return "Rolled " + str(self.value) + "."


class Box:
    """Holds the box value"""

    def __init__(self):
        self.value = 0

    def setToZero(self):
        self.value = 0

    def addValue(self, value_of_dice):
        self.value += value_of_dice


class Player(object):
    """Base class for different player types."""

    def __init__(self, name=None):
        self.name = name
        self.score = 0

    def add_score(self, player_score):
        """Adds score to total score."""

        self.score += player_score

    def __str__(self):
        """Returns player name and current score."""

        return str(self.name) + ": " + str(self.score)


class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)

    def keep_rolling(self, box):
        """Roll or hold"""

        human_decision = self.choices("  r - Roll again, h - Hold? ")
        if human_decision == "r":
            return True
        else:
            return False

    def choices(self, prompt='Please enter a Choice: '):
        """Takes input from user"""

        while True:
            choice = (input(prompt))
            if (choice != "r" and choice != "h"):
                print("Enter a valid choice")
            else:
                break
        return choice


class ComputerPlayer(Player):

    def __init__(self, number):
        """Give the computer player a name eg computer player 1"""

        name = 'Computer Player {}'.format(number + 1)

        super(ComputerPlayer, self).__init__(name)

    def keep_rolling(self, box):
        """Shows when the computer will roll or hold"""
        if box.value < 25 or box.value < 100 - self.score:
            print("CPU will hold.")
            return False
        else:
            print("CPU will roll again.")
            return True


class Play:
    def __init__(self, humanPlayers, computerPlayers):
        """Starts the game by asking names of players"""

        self.players = []

        for i in range(humanPlayers):
            player_name = input('Player {}, enter your name: '.format(i + 1))
            self.players.append(HumanPlayer(player_name))
        for i in range(computerPlayers):
            self.players.append(ComputerPlayer(i))

        print(self.players)

        self.no_of_players = len(self.players)

        self.die = Die()
        self.box = Box()

    def firstPlayer(self):
        """Player to begin"""
        self.current_player = 0 % self.no_of_players

    def nextPlayer(self):
        """The next player"""
        self.current_player = (self.current_player + 1) % self.no_of_players

    def previousPlayer(self):
        """The previous player"""
        self.current_player = (self.current_player - 1) % self.no_of_players

    def get_all_scores(self):
        """Returns a join all players scores."""

        return ', '.join(str(player) for player in self.players)

    def startGame(self):
        """Plays an entire game."""

        self.firstPlayer()

        while all(player.score < 100 for player in self.players):
            print('\n Current score > {}'.format(self.get_all_scores()))
            self.box.setToZero()

            print("-------{} First Roll------  ".format(self.players[self.current_player].name))
            while self.keep_rolling():
                pass

            self.players[self.current_player].add_score(self.box.value)
            self.nextPlayer()

        self.previousPlayer()
        print(' {} has won the game. Hurraay!! '.format(self.players[self.current_player].name).center(70, '*'))

    def keep_rolling(self):
        """ Check if play wants to roll. Set box to zero if dice rolls one"""
        try:
            value_of_dice = self.die.roll()
            self.box.addValue(value_of_dice)
            print('Last roll: {}, New Turn Total: {}'.format(value_of_dice, self.box.value))

            # do you want to keep rolling?
            return self.players[self.current_player].keep_rolling(self.box)

        except ExceptionforOne:
            print('Oops, Rolled a one. Changing Player')
            self.box.setToZero()
            return False


def main():
    # Initialize parser
    commandParser = argparse.ArgumentParser(description="Send a ­­url parameter to the script")
    # add parameter for file
    commandParser.add_argument("--player1", type=str, help="Number of Human players")
    commandParser.add_argument("--player2", type=str, help="Number of Computer players")
    args = commandParser.parse_args()

    human_players = int(args.player1)  # no of human players
    computer_players = int(args.player2)  # no of computer players

    startGame = Play(human_players, computer_players)
    startGame.startGame()


if __name__ == '__main__':
    main()