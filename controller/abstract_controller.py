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

    def play_turn(self, row, col):
        game_ended = False
        while not self.model.is_legal_move(self.model.board, self.model.curr_player, row, col):
            self.view.display_illegal_move()
            return -1

        self.model.make_move(self.model.board, self.model.curr_player, row, col)
        if self.model.is_board_full():
            game_ended = True
        else:
            self.model.change_turn()
            # if there are no legal moves for both players, game ends
            if not self.model.has_legal_moves():
                self.view.display_no_legal_moves(self.model.curr_player)
                self.model.change_turn()
                if not self.model.has_legal_moves():
                    self.view.display_no_legal_moves(0)
                    game_ended = True

        if game_ended:
            self.view.display_board()
            winner = self.model.get_winner()
            self.view.display_winner(winner)
        else:
            self.view.display_board()
            self.view.display_curr_player(self.model.curr_player)

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
