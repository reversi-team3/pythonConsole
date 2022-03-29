from model.AiStrategy import AiStrategy


class MediumAi(AiStrategy):
    def determine_move(self, board):
        return super().determine_move(board, 3)
