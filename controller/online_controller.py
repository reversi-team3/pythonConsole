from controller.abstract_controller import Controller
from model.model_proxy import ModelProxy

class OnlineController(Controller):
    def __init__(self, model: ModelProxy):
        super().__init__(model)


    def reset_game(self):
        size = self.model.board.shape[0]
        # FIXME shouldn't be initializing a game from inside the controller
        self.model = ModelProxy()
        self.model.set_board_size(size)
        # self.model.set_board_size(self.model.board.shape[0])
