from controller import Controller
from model import AiStrategy
from model.game_model import Game


class AiController(Controller):
    def __init__(self, model: Game):
        super.__init__(model)
        self.ai_difficulty = None

    def run_game(self):
        pass

    def play_turn(self, row, col):
        super.play_turn(row, col)
        if not self.model.is_board_full():
            self.play_turn(self.get_move())

    def get_move(self):
        return self.ai_difficulty.determine_move(self.model.board)

    def set_difficulty(self, ai_difficulty: AiStrategy):
        self.ai_difficulty = ai_difficulty
