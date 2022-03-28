from abc import ABC, abstractmethod


class GameView(ABC):
    def __init__(self, board, controller):
        self.board = board
        self.controller = controller

    @abstractmethod
    def display_board(self):
        pass

    @abstractmethod
    def display_curr_player(self, player):
        pass

    @abstractmethod
    def request_move(self, i=None, j=None):
        """ Asks for next move from user """
        pass

    @abstractmethod
    def display_illegal_move(self):
        """ Displays that the attempted move was illegal """
        pass

    @abstractmethod
    def display_winner(self, winner):
        """ Displays the winning Player """
        pass

    @abstractmethod
    def display_no_legal_moves(self, player):
        """ Displays a message that the given Player or both Players have no legal moves. """
        pass

    @abstractmethod
    def display_exit(self):
        pass
