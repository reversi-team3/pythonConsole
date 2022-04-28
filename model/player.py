from abc import abstractmethod
from enum import IntEnum


class Player(IntEnum):
    X = 1
    O = 2


player_symbol = {
    Player.X: 'black',
    Player.O: 'white'
}

base_player = Player.X
ai_player = Player.O

class BasePlayer:
    def __init__(self, color: Player):
        super().__init__()
        self.color = color


        @abstractmethod
        def receive_move(self):
            pass


        @abstractmethod
        def get_received_move(self):
            pass
