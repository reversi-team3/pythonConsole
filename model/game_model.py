import numpy as np
from model.player import Player
#from mysql.connector import connect, Error
from getpass import getpass


class Game:
    def __init__(self):
        self.board = 0
        self.curr_player = Player.X
        self.set_board_size()
        # used for runtime efficiency of has_legal_moves()
        self.zeros = self.board.size - 4
        # should probably initialize the db server connection here and refer to it as needed
        # instead of opening/closing in every method call

    def set_board_size(self, board_size=8):
        self.board = np.zeros((board_size, board_size), dtype=np.int)
        self.board[int(board_size / 2), int(board_size / 2)
                   ] = int(self.curr_player)
        self.board[int(board_size / 2 - 1), int(board_size / 2 -
                                                1)] = int(self.curr_player)
        self.board[int(board_size / 2), int(board_size / 2 - 1)
                   ] = int(1 + self.curr_player)
        self.board[int(board_size / 2 - 1), int(board_size / 2)
                   ] = int(1 + self.curr_player)

    @staticmethod
    def is_legal_move(board, curr_turn, row, col):
        if row < 0 or row >= len(board):
            return False
        if col < 0 or col >= len(board):
            return False
        if board[row, col] != 0:
            return False

        else:
            # Generating the list of neighbours
            neighbour = False
            neighbours = []
            for i in range(max(0, row-1), min(row+2, len(board))):
                for j in range(max(0, col-1), min(col+2, len(board))):
                    if board[i][j] != 0:
                        neighbour = True
                        neighbours.append([i, j])
            # If there's no neighbours, it's an invalid move
            if not neighbour:
                return False
            else:
                valid = False
                # Finds straight line to another curr_player disk
                for neighbour in neighbours:

                    neighbor_x = neighbour[0]
                    neighbor_y = neighbour[1]

                    # If the neighbour colour is equal to your colour, it doesn't form a line
                    # Go onto the next neighbour
                    if board[neighbor_x][neighbor_y] == curr_turn:
                        continue
                    else:
                        # Direction of the line
                        x_increment = neighbor_x-row
                        y_increment = neighbor_y-col
                        temp_x = neighbor_x
                        temp_y = neighbor_y

                        while 0 <= temp_x < len(board) and 0 <= temp_y < len(board):
                            # if empty tile, no line can be formed
                            if board[temp_x][temp_y] == 0:
                                break
                            # Line formed
                            if board[temp_x][temp_y] == curr_turn:
                                valid = True
                                break
                            # Move the index according to the direction of the line
                            temp_x += x_increment
                            temp_y += y_increment
                return valid

    @staticmethod
    def make_move(board, curr_turn, row, col):
        board[row, col] = int(curr_turn)
        neighbours = []
        for i in range(max(0, row - 1), min(row + 2, len(board))):
            for j in range(max(0, col - 1), min(col + 2, len(board))):
                if board[i][j] != 0:
                    neighbours.append([i, j])

        # Which tiles to flip
        flip = []

        # For all the generated neighbours, determine if they form a line
        # If a line is formed, we will add it to the convert array
        for neighbour in neighbours:
            neighbor_x = neighbour[0]
            neighbor_y = neighbour[1]
            # Check if the neighbour is of a different colour - it must be to form a line
            if board[neighbor_x][neighbor_y] != curr_turn:
                # The path of each individual line
                path = []

                # Determining direction to move, will be from -1 to 1
                x_increment = neighbor_x - row
                y_increment = neighbor_y - col

                temp_x = neighbor_x
                temp_y = neighbor_y

                # While we are in the bounds of the board
                while 0 <= temp_x < len(board) and 0 <= temp_y < len(board):
                    path.append([temp_x, temp_y])
                    value = board[temp_x][temp_y]
                    # If we reach a blank tile, we're done and there's no line
                    if value == 0:
                        break
                    # If we reach a tile of the player's colour, a line is formed
                    if value == curr_turn:
                        # Append all of our path tiles to the convert array
                        for tile in path:
                            flip.append(tile)
                        break
                    # Move the tile
                    # self.board[tempX][tempY] = self.curr_player
                    temp_x += x_increment
                    temp_y += y_increment

        # Convert all the appropriate tiles
        for tile in flip:
            board[tile[0]][tile[1]] = curr_turn
            # re-implement zeros

    def has_legal_moves(self):
        """
        :return: True if there are still legal moves for this player, false otherwise
        """
        if self.zeros >= len(self.board):
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 0 and Game.is_legal_move(self.board, self.curr_player, i, j):
                        return True
        else:
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] != 0:
                        zeros = self.has_surrounding_empty_tile(i, j)
                        if zeros:
                            for zero in zeros:
                                if Game.is_legal_move(self.board, self.curr_player, zero[0], zero[1]):
                                    return True
            return False

    def has_surrounding_empty_tile(self, row, col):
        neighbor_zeros = []
        for i in range(max(0, row - 1), min(row + 2, len(self.board))):
            for j in range(max(0, col - 1), min(col + 2, len(self.board))):
                if self.board[i][j] == 0:
                    neighbor_zeros.append([i, j])
        return neighbor_zeros

    def is_board_full(self):
        return not np.any(self.board == 0)

    def change_turn(self):
        if self.curr_player == 1:
            self.curr_player = Player(2)
        else:
            self.curr_player = Player(1)

    def get_winner(self):
        """
        :return: 1 if Player X won, 2 if Player O won, 0 if draw
        """
        player_one_disks = 0
        player_two_disks = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == Player.X:
                    player_one_disks += 1
                if self.board[i][j] == Player.O:
                    player_two_disks += 1

        # update wins and losses for winner
        if player_one_disks > player_two_disks:
            return Player.X
        elif player_one_disks < player_two_disks:
            return Player.O
        else:
            return 0

    def get_leaderboard(self):
        # try/catch this
        conn = connect()

        lb_query = "SELECT * FROM leaderboard"
        with conn.cursor as cursor:
            cursor.execute(lb_query)
            result = cursor.fetchall()
            return result
