from model.model import Game
from view.game_view import GameView


class LocalController:
    def __init__(self, model: Game, view: GameView):
        self.model = model
        self.view = view

    def run_game(self):
        game_ended = False

        while not game_ended:
            self.view.display_board()
            self.view.display_curr_player(self.model.curr_player)

            row, col = self.view.get_move()
            if [row, col] == [-1, -1]:
                print("Exiting.")
                return

            while not self.model.is_legal_move(row, col):
                self.view.display_illegal_move()
                row, col = self.view.get_move()

            self.model.make_move(row, col)
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

        self.view.display_board()
        winner = self.model.get_winner()
        self.view.display_winner(winner)
