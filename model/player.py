from enum import IntEnum

class Player(IntEnum):
    X = 1
    O = 2

player_symbol = {
    Player.X: 'X',
    Player.O: 'O'
}