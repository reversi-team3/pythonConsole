from abc import ABC, abstractmethod

import numpy

from model.game_model import Game
from model.player import Player


class AiStrategy(ABC):
    def determine_move(self, board, depth):
        valid_moves = self.get_move_list(board)
        move_values = []
        if len(valid_moves) == 0:
            return -1, -1

        for move in valid_moves:
            val = self.minimax(board, move, depth, Player.O)
            move_values.append(val)
        index = move_values.index(max(move_values))
        return valid_moves[index]

    def get_move_list(self, board):
        valid_moves = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0 and Game.is_legal_move(self.board, Player.O, i, j):
                    valid_moves.append([i, j])
        return valid_moves

    # returns score of board in favor of player o (ai)
    def score(self, board):
        player_x_disks = 0
        player_o_disks = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == Player.X:
                    player_x_disks += 1
                if board[i][j] == Player.O:
                    player_o_disks += 1

        return player_o_disks - player_x_disks

    def minimax(self, board, curr_move, depth, player):
        board_copy = [[]]
        numpy.copyto(board_copy, board)
        Game.make_move(board_copy, player, curr_move[0], curr_move[1])

        if depth == 0 or not numpy.any(board_copy == 0):
            self.score(board_copy)
        if player == Player.O:  # maximizing Player O (AI)'s move
            max_val = -999999999
            moves = self.get_move_list(board_copy)
            for move in moves:
                val = self.minimax(board_copy, move, depth - 1, Player.X)
                max_val = max(max_val, val)
            return max_val
        else:
            min_val = 999999999
            moves = self.get_move_list(board_copy)
            for move in moves:
                val = self.minimax(board_copy, move, depth - 1, Player.O)
                min_val = min(min_val, val)
            return min_val





