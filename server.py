import socket
import pickle
import threading
from model.game_model import Game
from database.ActiveGameManager import ActiveGameManager
from database.DBManager import DBManager


class Server:
    def __init__(self, host='127.0.0.1', port=3456, buffer_size=1024):
        self.models = {} # Model -> (Username, Port), (Username, Port)
        # self.players = OrderedDict() # PlayerObject -> Model
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.ActiveGamesManager = ActiveGameManager(DBManager.get_instance())

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()

            while True:
                conn, address = my_socket.accept()
                self.models[address] = Game() # get_model
                thread = threading.Thread(target=self.handle_client, args=(conn, address))
                thread.start()

# """ TODO: possibly sending model to server, since players are changing, colors are changing, etc
#     def get_model(self, model):
#         return model
# """
    def handle_client(self, conn, address):
        with conn:
            while True:
                binary = conn.recv(self.buffer_size)
                if not binary:
                    break
                msg = pickle.loads(binary)

                model = self.models[address]
                if not model:
                    break
                print('Here')
                result = (Server.delegate(self, model, msg), model)
                print(result)
                result_binary = pickle.dumps(result)
                conn.sendall(result_binary)

    def delegate(self, model: Game, msg):
        msg_name = msg[0]
        if msg_name == "set_board_size":
            model.set_board_size(msg[1])
            return model.game_state
        elif msg_name == "is_legal_move":
            return model.is_legal_move(msg[1], msg[2], msg[3], msg[4])
        elif msg_name == "make_move":
            return model.make_move(msg[1], msg[2])
        elif msg_name == "has_legal_moves":
            return model.has_legal_moves()
        elif msg_name == "has_surrounding_empty_tile":
            return model.has_surrounding_empty_tile(msg[1], msg[2])
        elif msg_name == "is_board_full":
            return model.is_board_full()
        elif msg_name == "change_turn":
            return model.change_turn()
        elif msg_name == "get_winner":
            return model.get_winner()
        elif msg_name == "get_leaderboard":
            return model.get_leaderboard()
        elif msg_name == "get_to_JSON":
            return model.to_JSON()
        elif msg_name == "get_from_JSON":
            return model.from_JSON()
        elif msg_name == "update_active_game":
            return model.update_active_game(self.ActiveGamesManager)
        elif msg_name == "add_game_to_active_games":
            return model.add_game_to_active_games(self.ActiveGamesManager)
        return None


if __name__ == "__main__":
    server = Server()
    server.start()
