from model.player import BasePlayer, player_color, Color


class OnlinePlayer(BasePlayer):
    def __init__(self, username, color: Color):
        super().__init__(color)
        self.username = username
        #self.elo = self.get_elo
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
