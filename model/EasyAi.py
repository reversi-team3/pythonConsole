from model.AiStrategy import AiStrategy


class EasyAi(AiStrategy):
    def determine_move(self, board):
        return super().determine_move(board, 1)
