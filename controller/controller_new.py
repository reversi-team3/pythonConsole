from model.game_model import Game
from view.game_view import GameView
from model.player import Player


class NewController:
    def __init__(self, model: Game, view: GameView):
        self.model = model
        self.view = view
        self.players = [self.model.player_one, self.model.player_two]

    def run_game(self):
        game_ended = False

        while not game_ended:
            self.view.display_board()
            self.view.display_curr_player(self.model.curr_player)

            row, col = self.get_move()
            if [row, col] == [-1, -1]:
                self.view.display_exit()
                return

            while not self.model.is_legal_move(row, col):
                self.view.display_illegal_move()
                row, col = self.get_move()

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

    def get_move(self):
        move = [0]
        valid = False
        while len(move) != 2 and not valid:
            move = self.view.request_move()
            if move == "exit":
                return [-1, -1]
            try:
                move = move.split(',')
                row = int(move[0]) - 1
                col = int(move[1]) - 1
                valid = True
            except (ValueError, IndexError) as e:
                self.view.display_illegal_move()
                move = [0]
                continue
        return row, col

    def update_board(self):
        self.view.display_board()

        if not self.model.is_board_full():
            self.view.display_curr_player(self.model.curr_player)
        else:
            self.game_over()

    def game_over(self):
        self.view.display_board()
        self.view.display_winner(self.model.get_winner())

