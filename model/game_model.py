import ast
import json
import math

import numpy as np

from database.ActiveGameManager import ActiveGameManager
# kihang add
from database.DBManager import DBManager
from model.online_player import OnlinePlayer
from model.player import BasePlayer, Color
from mysql.connector import connect, Error
from getpass import getpass
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class Game:
    def __init__(self, *args):
        
        if len(args) > 2:
            self.player_one = args[0]
            self.player_two = args[1]
            self.board = args[2]
            if args[3] == self.player_one.username:
                self.curr_player = self.player_one
            else:
                self.curr_player = self.player_two
        else:
            if args:
                self.player_one = args[0]
                self.player_two = args[1]

            else:
                self.player_one = OnlinePlayer("Guest", Color.BLACK, 1)
                self.player_two = OnlinePlayer("Player2", Color.WHITE)
            self.board = 0
            self.curr_player = self.player_one
            self.set_board_size()
            # used for runtime efficiency of has_legal_moves()
        self.zeros = len(self.board) - 4
            #self.db = None
            # should probably initialize the db server connection here and refer to it as needed
            # instead of opening/closing in every method call
        self.db = DBManager.get_instance()


    # not sure if this is necessary
    def set_db(self, db):
        self.db = db

    def set_board_size(self, board_size=8):
        self.board = np.zeros((board_size, board_size), dtype=np.object)
        self.board[int(board_size / 2), int(board_size / 2)
        ] = self.player_one.num
        self.board[int(board_size / 2 - 1), int(board_size / 2 -
                                                1)] = self.player_one.num
        self.board[int(board_size / 2), int(board_size / 2 - 1)
        ] = self.player_two.num
        self.board[int(board_size / 2 - 1), int(board_size / 2)
        ] = self.player_two.num

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
            for i in range(max(0, row - 1), min(row + 2, len(board))):
                for j in range(max(0, col - 1), min(col + 2, len(board))):
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
                        x_increment = neighbor_x - row
                        y_increment = neighbor_y - col
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
        board[row, col] = curr_turn
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
                    if self.board[i][j] == 0 and Game.is_legal_move(self.board, self.curr_player.num, i, j):
                        return True
        else:
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] != 0:
                        zeros = self.has_surrounding_empty_tile(i, j)
                        if zeros:
                            for zero in zeros:
                                if Game.is_legal_move(self.board, self.curr_player.num, zero[0], zero[1]):
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
        if self.curr_player == self.player_one:
            self.curr_player = self.player_two
        else:
            self.curr_player = self.player_one

    def get_winner(self):
        """
        :return: 1 if Player X won, 2 if Player O won, 0 if draw
        """
        self.db.deleteGame(self.player_one.username)
        player_one_disks = 0
        player_two_disks = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == self.player_one.num:
                    player_one_disks += 1
                if self.board[i][j] == self.player_two.num:
                    player_two_disks += 1

        # update wins and losses for winner
        if player_one_disks > player_two_disks:
            return self.player_one
        elif player_one_disks < player_two_disks:
            return self.player_two
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

    def to_JSON(self):
        json_board = self.board.tolist()
        json_board = json.dumps(json_board)
        return json.dumps(json_board, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
        # return json.dumps(self, default=vars,
        #                   sort_keys=True, indent=4)

    def from_JSON(self):
        self.board = np.array(json.loads(json.loads(self.board)))

# """
#     def add_game_to_active_games(self):
#         pass

#     def update_active_game(self, db: ActiveGameManager):
#         db.updateGame("Frank", "John", self.to_JSON())
#         self.from_JSON()
# """
    # def add_game_to_active_games(self, db: ActiveGameManager):
    #     db.addGame("Frank", "John", self.to_JSON())
    #     self.from_JSON()

    # def update_active_game(self, db: ActiveGameManager):
    #     db.updateGame("Frank", "John", self.to_JSON())
    #     self.from_JSON()

    def get_player(self, num):
        if self.player_one.num == num:
            return self.player_one
        else:
            return self.player_two

    def set_player_elo(self):
        self.player_one.elo = self.db.getElo(self.player_one.username)
        # set player_two elo

    def update_elo(self, winner):
        if winner == self.player_one:
            player_one_elo = self.player_one.update_elo(self.player_two.elo, True)
            player_two_elo = self.player_two.update_elo(self.player_one.elo, False)
        else:
            player_one_elo = self.player_one.update_elo(self.player_two.elo, False)
            player_two_elo = self.player_two.update_elo(self.player_one.elo, True)

        self.db.updateElo(self.player_one.username, player_one_elo)
        self.db.updateElo(self.player_two.username, player_two_elo)

        # questionable logic
        #winner.elo = 30 + winner.elo * (1 - probability)
        #loser.elo = 30 + loser.elo * (0 - probability)