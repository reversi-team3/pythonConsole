from abc import ABC, abstractmethod
import numpy
import numpy as np
from model.game_model import Game
from model.player import Player


class AiStrategy(ABC):
    def determine_move(self, board, depth):
        valid_moves = self.get_move_list(board)
        move_values = []
        if len(valid_moves) == 0:
            return -1, -1
        alpha = -999999999
        beta = 999999999
        for move in valid_moves:
            val = self.minimax(board, move, depth, Player.O, alpha, beta)
            move_values.append(val)
        index = move_values.index(max(move_values))
        return valid_moves[index]

    def get_move_list(self, board):
        valid_moves = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0 and Game.is_legal_move(board, Player.O, i, j):
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

    def minimax(self, board, curr_move, depth, player, alpha, beta):
        board_copy = np.copy(board)
        Game.make_move(board_copy, player, curr_move[0], curr_move[1])

        if depth <= 0 or not numpy.any(board_copy == 0):
            return self.score(board_copy)
        if player == Player.O:  # maximizing Player O (AI)'s move
            max_val = -999999999
            moves = self.get_move_list(board_copy)
            for move in moves:
                val = self.minimax(board_copy, move, depth - 1, Player.X, alpha, beta)
                max_val = max(max_val, val)
                if max_val >= beta:
                    return max_val
                alpha = max(alpha, max_val)
            return max_val
        else:
            min_val = 999999999
            moves = self.get_move_list(board_copy)
            for move in moves:
                val = self.minimax(board_copy, move, depth - 1, Player.O, alpha, beta)
                min_val = min(min_val, val)
                if min_val <= alpha:
                    return min_val
                beta = min(beta, min_val)
            return min_val