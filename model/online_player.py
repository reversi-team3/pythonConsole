import math

from model.player import BasePlayer, player_color, Color


class OnlinePlayer(BasePlayer):
    def __init__(self, username, color: Color, number=2):
        super().__init__(color)
        self.username = username
        self.elo = 1500 # pull elo from DB
        # i think they need value??
        self.num = number
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

    def set_elo(self, elo):
        self.elo = elo

    def update_elo(self, opponent_rating, self_won):
        probability = 1 * 1 / (1 + 1 * math.pow(10, 1 * (opponent_rating - self.elo) / 400)) # get probability of self winning
        if self_won:
            self.elo = abs(int(30 + self.elo * (1 - probability)))
        else:
            self.elo = abs(int(30 + self.elo * (0 - probability)))

        return self.elo

        # update database

