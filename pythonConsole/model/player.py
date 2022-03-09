from enum import IntEnum


class Player(IntEnum):
    X = 1
    O = 2


player_symbol = {
    Player.X: 'black',
    Player.O: 'white'
}
