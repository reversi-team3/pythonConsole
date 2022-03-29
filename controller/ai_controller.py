import time

from controller.controller import Controller
from model.AiStrategy import AiStrategy
from model.game_model import Game
from model.player import Player


class AiController(Controller):
    def __init__(self, model: Game):
        super().__init__(model)
        self.ai_difficulty = None

    def run_game(self):
        pass

    def play_turn(self, row, col):
        super().play_turn(row, col)
        # self.view.display_curr_player(Player.O)
        time.sleep(.5)
        if not self.model.is_board_full():
            move = self.get_move()
            super().play_turn(move[0], move[1])

    def get_move(self):
        move = self.ai_difficulty.determine_move(self.model.board)
        return move

    def set_difficulty(self, ai_difficulty: AiStrategy):
        self.ai_difficulty = ai_difficulty
