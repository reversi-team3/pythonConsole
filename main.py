from enum import Enum

from GUIView import GUIView
from controller.controller_new import NewController
from model.game_model import Game
from view.game_console_view import GameConsoleView
from database import DBManager

if __name__ == "__main__":
    exec(open("./GUIView.py").read())


