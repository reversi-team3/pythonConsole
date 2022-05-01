import ast
import json
import math
from abc import abstractmethod, ABC

import numpy as np

from database.ActiveGameManager import ActiveGameManager
# kihang add
from database.DBManager import DBManager
from model.online_player import OnlinePlayer
from model.player import BasePlayer, Color
from mysql.connector import connect, Error
from getpass import getpass


class AGame(ABC):
    def __int__(self):
        pass

    @abstractmethod
    def set_board_size(self, board_size=8):
        pass

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

    @abstractmethod
    def has_legal_moves(self):
        """
        :return: True if there are still legal moves for this player, false otherwise
        """
        pass

    @abstractmethod
    def has_surrounding_empty_tile(self, row, col):
        pass

    @abstractmethod
    def is_board_full(self):
        pass

    @abstractmethod
    def change_turn(self):
        pass

    @abstractmethod
    def get_winner(self):
        """
        :return: 1 if Player X won, 2 if Player O won, 0 if draw
        """
        pass

    @abstractmethod
    def get_leaderboard(self):
        pass

    @abstractmethod
    def to_JSON(self):
        pass

    @abstractmethod
    def from_JSON(self):
        pass

    @abstractmethod
    def get_player(self, num):
        pass

    @abstractmethod
    def set_player_elo(self):
        pass

    @abstractmethod
    def update_elo(self, winner):
        pass

    @abstractmethod
    def get_online_players(self):
        pass