import socket
import pickle

from model.AModel import AGame
from model.game_model import Game
from model.player import Player


class ModelProxy(AGame):
    def __init__(self, username, server='127.0.0.1', port=3000, buffer_size=1024):
        self.socket = socket.socket()
        self.socket.connect((server, port))
        self.buffer_size = buffer_size

        self.board = 0

        self.player_one = username
        self.send(("add_active_player", self.player_one.username))
        self.player_two = None

        self.curr_player = self.player_one

        # self.set_board_size()

    def send(self, msg):
        binary = pickle.dumps(msg)
        self.socket.sendall(binary)
        result_binary = self.socket.recv(self.buffer_size)
        # print(pickle.loads(result_binary))
        board, curr_player = pickle.loads(result_binary)
        self.update_self(board, curr_player)
        return board

    def update_self(self, board, curr_player):
        self.board = board
        self.curr_player = curr_player

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

    def get_player(self, num):
        msg = ("get_player", num)
        return self.send(msg)

    def set_player_elo(self):
        msg = ("set_player_elo",)
        return self.send(msg)

    def update_elo(self, winner):
        msg = ("update_elo", winner)
        return self.send(msg)

    def connect_to_game(self, player):
        msg = ("connect_to_game", player)
        return self.send(msg)

    def get_online_players(self):
        msg = ("get_online_players",)
        return self.send(msg)

    def add_online_session(self, username1, username2):
        msg = ("add_online_session", username1, username2)
        return self.send(msg)

    def accept_session(self, username):
        msg = ("accept_session", username)
        return self.send(msg)

