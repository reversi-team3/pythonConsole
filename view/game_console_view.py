from view.game_view import GameView
from model.player import player_symbol


class GameConsoleView(GameView):
    def __init__(self, board_view):
        super().__init__(board_view)

    def display_curr_player(self, player):
        print(f"Player {player_symbol[player]}'s turn.")

    def get_move(self):
        move = [0]
        while len(move) != 2:
            move = input("Enter your move (row, col): ")
            if move == "exit":
                return [-1, -1]
            move = move.split(',')
            if len(move) != 2:
                self.display_illegal_move()
        row = int(move[0]) - 1
        col = int(move[1]) - 1
        return row, col

    def display_illegal_move(self):
        print("This move is illegal. Try again.")
        # maybe display board here

    def display_no_legal_moves(self, player):
        if player == 0:
            print("No legal moves remaining for either player.")
        else:
            print(f'There are currently no legal moves for {player_symbol[player]}.')

    def display_winner(self, winner):
        if winner == 0:
            print("No legal moves remaining. Draw.")
        else:
            print(f'Player {player_symbol[winner]} has won the game! Congratulations!')
