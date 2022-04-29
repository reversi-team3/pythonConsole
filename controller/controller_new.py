from model.game_model import Game
from model.local_player import LocalPlayer
from model.player import Color
from view.game_view import GameView


class NewController:
    def __init__(self, model: Game):
        self.model = model
        self.view = None

    def set_view(self, view: GameView):
        self.view = view

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

    def play_turn(self, row, col):
        game_ended = False
        while not self.model.is_legal_move(self.model.board, self.model.curr_player.num, row, col):
            self.view.display_illegal_move()
            return -1

        self.model.make_move(self.model.board, self.model.curr_player.num, row, col)
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

    def change_board_size(self, new_size):
        if (new_size % 2) != 0 or new_size < 6:
            return -1
        if self.view is not None:
            self.model.set_board_size(new_size)

    def get_move(self):
        move = [0]
        valid = False
        while len(move) != 2 and not valid:
            move = self.model.curr_player.receive_move()
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
        self.model.player_one.update_elo(self.model.player_two.elo, self.model.get_winner() == self.model.player_one)
        self.model.player_two.update_elo(self.model.player_one.elo, self.model.get_winner() == self.model.player_two)
        self.view.display_winner(self.model.get_winner())
        

    def reset_game(self, player_one, board = None, turn = None):
        if board:
            self.model = Game(player_one, LocalPlayer("Player2", Color.WHITE), board, turn)
            self.model.from_JSON()
            # print(self.model.board)
        else:
            self.model = Game(self.model.player_one, self.model.player_two)
            size = self.model.board.shape[0]
            self.model.set_board_size(size)
       
        # FIXME shouldn't be initializing a game from inside the controller
        self.model.player_two.set_game(self.model)
        self.model.set_player_elo()
        # self.model.set_board_size(self.model.board.shape[0])

    def add_active_game_to_db(self):
        self.model.db.addGame(self.model.player_one.username, self.model.player_two.username, self.model.to_JSON())

    def update_active_game(self):
        self.model.db.updateGame(self.model.player_one.username, self.model.to_JSON(), self.model.curr_player.username)


