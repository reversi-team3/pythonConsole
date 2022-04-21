import socket
import pickle
import threading

from model.game_model import Game

class Server:
    def __init__(self, host='127.0.0.1', port=3000, buffer_size=1024):
        self.models = {}
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()

            while True:
                conn, address = my_socket.accept()
                self.models[address] = Game()
                thread = threading.Thread(target=self.handle_client, args=(conn,address))
                thread.start()

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
                result = (Server.delegate(model, msg), model)
                result_binary = pickle.dumps(result)
                conn.sendall(result_binary)

    @staticmethod
    def delegate(model: Game, msg):
        msg_name = msg[0]
        if msg_name == "set_board_size":
            return model.set_board_size(msg[1])
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
        return None


if __name__ == "__main__":
    server = Server()
    server.start()
