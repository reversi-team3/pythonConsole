from abc import ABC, abstractmethod
from enum import IntEnum, Enum


class Player(IntEnum):
    X = 1
    O = 2


player_symbol = {
    Player.X: 'black',
    Player.O: 'white'
}

player_color = {
    'black',
    'white',
    'blue',
    'purple'
}


class Color(Enum):
    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    WHITE = "white"
    PURPLE = "purple"


base_player = Player.X
ai_player = Player.O  # ai_player is always going to be Player.O


class BasePlayer(ABC):
    def __init__(self, color: Color):
        super().__init__()
        self.color = color
        self.elo = 0

    # Returns the user's move
    @abstractmethod
    def receive_move(self) -> (int, int):
        pass

    @abstractmethod
    def update_elo(self, opponent_rating, self_won):
        pass
