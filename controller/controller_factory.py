from controller.controller import Controller
from controller.ai_controller import AiController
from controller.local_controller import LocalController
from model.game_model import Game


class ControllerFactory:
    def get_controller(self, controller_type: str, model: Game) -> Controller:
        if controller_type == 'ai':
            return AiController(model)
        elif controller_type == 'local':
            return LocalController(model)
        raise ValueError('Unknown shape type')