from controller import Controller
from model import AiStrategy
from model.game_model import Game


class AiController(Controller):
    def __init__(self, model: Game):
        super.__init__(model)


    def run_game(self):
        pass

    def play_turn(self):
        pass

    def get_move(self):
        return self.ai_difficulty.determine_move(self.model.board)

    def set_difficulty(self, ai_difficulty: AiStrategy):
        pass