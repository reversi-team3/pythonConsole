import math

from model.player import BasePlayer, player_color, Color


class OnlinePlayer(BasePlayer):
    def __init__(self, username, color: Color):
        super().__init__(color)
        self.username = username
        self.elo = 1500 # pull elo from DB
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
        probability = 1 * 1 // (1 + 1 * math.pow(10, 1 * (opponent_rating - self.elo) // 400)) # get probability of self winning
        if self_won:
            self.elo = 30 + self.elo * (1 - probability)
        else:
            self.elo = 30 + self.elo * (0 - probability)

        # update database
