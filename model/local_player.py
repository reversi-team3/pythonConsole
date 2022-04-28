import math

from model.player import BasePlayer, player_color, Color


class LocalPlayer(BasePlayer):
    def __init__(self, username, color: Color):
        super().__init__(color)
        self.username = username
    """
    def get_elo(self):
        # self.elo = pull from db
        return elo
    """
    def change_color(self, color):
        self.color = Color(color)

    def receive_move(self, i, j):
        return i, j

    def set_game(self, model):
        pass

    def update_elo(self, opponent_rating, self_won):
        pass

