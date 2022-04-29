import socket
import pickle

from model.game_model import Game
from model.player import Player


class ModelProxy:
    def __init__(self, player, server='127.0.0.1', port=3000, buffer_size=1024):
        self.socket = socket.socket()
        self.socket.connect((server, port))
        self.buffer_size = buffer_size

        self.board = 0
        self.curr_player = player
        self.set_board_size()
        self.zeros = self.board.size - 4

    def send(self, msg):
        binary = pickle.dumps(msg)
        self.socket.sendall(binary)
        result_binary = self.socket.recv(self.buffer_size)
        response, new_self = pickle.loads(result_binary)
        self.update_self(new_self)
        return response

    def update_self(self, new_self):
        self.board = new_self.board
        self.curr_player = new_self.curr_player
        self.zeros = new_self.zeros

    def set_board_size(self, board_size=8):
        msg = ("set_board_size", board_size)
        return self.send(msg)

    @staticmethod
    def is_legal_move(board, curr_turn, row, col):
        return Game.is_legal_move(board, curr_turn, row, col)

    @staticmethod
    def make_move(board, curr_turn, row, col):
        return Game.make_move(board, curr_turn, row, col)

    def has_legal_moves(self):
        msg = "has_legal_moves"
        return self.send(msg)

    def has_surrounding_empty_tile(self, row, col):
        msg = ("has_surrounding_empty_tile", row, col)
        return self.send(msg)

    def is_board_full(self):
        msg = "is_board_full"
        return self.send(msg)

    def change_turn(self):
        msg = "change_turn"
        return self.send(msg)

    def get_winner(self):
        msg = "get_winner"
        return self.send(msg)

    def get_leaderboard(self):
        msg = "get_leaderboard"
        return self.send(msg)

    def to_JSON(self):
        msg = ("get_to_JSON",)
        return self.send(msg)

    def from_JSON(self):
        msg = ("get_from_JSON",)
        return self.send(msg)

    def add_game_to_active_games(self):
        msg = ("add_game_to_active_games",)
        return self.send(msg)

    def update_active_game(self):
        msg = ("update_active_game",)
        return self.send(msg)