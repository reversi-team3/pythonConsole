from view.game_view import GameView
from model.player import player_symbol


class GameConsoleView(GameView):
    def __init__(self, board, controller: GameView):
        super().__init__(board, controller)

    def display_board(self):
        board_size = len(self.board)
        header_len = board_size * 4 + 1
        print("-" * header_len)
        for row in range(board_size):
            for col in range(board_size):
                if self.board[row, col] == 0:
                    cell = ' '
                else:
                    cell = player_symbol[self.board[row, col]]
                print(f'| {cell} ', end='')
            print('|')
        print("-" * header_len)

    def display_curr_player(self, player):
        print(f"Player {player_symbol[player]}'s turn.")

    def request_move(self, i=None, j=None):
        move = input("Enter your move (row, col): ")
        return move

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

    def display_exit(self):
        print("Exiting game.")