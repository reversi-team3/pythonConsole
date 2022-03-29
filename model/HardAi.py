from model.AiStrategy import AiStrategy


class HardAi(AiStrategy):
    def determine_move(self, board):
        return super().determine_move(board, 5)
