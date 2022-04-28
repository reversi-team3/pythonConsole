from abc import abstractmethod

from model.game_model import Game
from model.player import BasePlayer, Player
from view.game_view import GameView


class OnlinePlayer(BasePlayer):
    def __init__(self, view: GameView, color: Player):
        super().__init__(color)
        self.view = view

    def receive_move(self):
        return self.view.request_move(None, None)
