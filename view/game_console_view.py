from view.game_view import GameView
from model.player import player_symbol


class GameConsoleView(GameView):
    def __init__(self, board_view):
        super().__init__(board_view)

    def display_curr_player(self, player):
        print(f"Player {player_symbol[player]}: It's your turn.")

    def show_legal_moves(self):
        pass

    def get_move(self):
        move = input("Enter your move (row, col): ")
        move = move.split(',')
        row = int(move[0]) - 1
        col = int(move[1]) - 1
        return row, col

    def display_illegal_move(self):
        print("This move is illegal. Try again.")

    def display_winner(self, winner):
        if winner == 0:
            print("DRAW")
        else:
            print(f'Player {player_symbol[winner]} has won the game')
