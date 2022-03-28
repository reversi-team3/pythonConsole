from abc import ABC, abstractmethod

from model.game_model import Game
from view.game_view import GameView


class Controller(ABC):
    def __init__(self, model: Game):
        self.model = model
        self.view = None

    @abstractmethod
    def run_game(self):
        pass

    @abstractmethod
    def play_turn(self, row, col):
        pass

    @abstractmethod
    def get_move(self):
        pass

    def change_board_size(self, new_size):
        if (new_size % 2) != 0 or new_size < 6:
            return -1
        if self.view is not None:
            self.model.set_board_size(new_size)

    def reset_game(self):
        size = self.model.board.shape[0]
        self.model = Game()
        self.model.set_board_size(size)
        # self.model.set_board_size(self.model.board.shape[0])

    def set_view(self, view: GameView):
        self.view = view

    def get_leaderboard(self):
        return
