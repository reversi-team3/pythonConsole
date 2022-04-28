from enum import Enum

from GUIView import GUIView
from controller.local_controller import LocalController
from model.game_model import Game
from view.game_console_view import GameConsoleView
#main.py

"""
board_size = input("Welcome to Reversi!\n"
                   "Local mode selected.\n"
                   "Enter your game board size(at least 4, must be even): ")
while int(board_size) % 2 == 1:
    board_size = input("Invalid board size. Must be at least 4 and even: ")

print("Type \"exit\" at any time to exit the game.")
game = Game()

controller = LocalController(game)
game_view = GUIView(controller, game.board)
controller.set_view(game_view)
controller.run_game()
"""
class Color(Enum):
    RED = "red"
    BLUE = "blue"
    BLACK = "black"
    WHITE = "white"
    PURPLE = "purple"

print(Color.RED.value)