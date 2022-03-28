from model import AiStrategy


class EasyAi(AiStrategy):
    def determine_move(self, board):
        super.determine_move(self, board, 7)
