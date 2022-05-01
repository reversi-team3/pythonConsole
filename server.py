import socket
import pickle
import threading
from model.game_model import Game
from database.ActiveGameManager import ActiveGameManager
from database.DBManager import DBManager


class Server:
    def __init__(self, host='127.0.0.1', port=3000, buffer_size=1024):
        self.models = {}  # address -> Game
        self.online_sessions = {}  # (username1, username2) -> Game
        self.address_to_session = {}  # address -> (username1, username2)
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.db = DBManager.get_instance()

    def start(self):
        with socket.socket() as my_socket:
            my_socket.bind((self.host, self.port))
            my_socket.listen()

            while True:
                conn, address = my_socket.accept()
                self.models[address] = Game()  # get_model
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

                if address not in self.address_to_session:
                    model = self.models[address]
                else:
                    session = self.address_to_session[address]
                    model = self.online_sessions[session]
                    print(model.id)
                if not model:
                    break
                print('Here')
                result = (Server.delegate(self, model, msg, address))
                print(result)
                result_binary = pickle.dumps(result)
                conn.sendall(result_binary)

    def delegate(self, model: Game, msg, address):
        msg_name = msg[0]
        if msg_name == "set_board_size":
            model.set_board_size(msg[1])
            return model.game_state
        elif msg_name == "is_legal_move":
            model.is_legal_move(msg[1], msg[2], msg[3], msg[4])
            return model.game_state
        elif msg_name == "make_move":
            model.make_move(msg[1], msg[2])
            return model.game_state
        elif msg_name == "has_legal_moves":
            model.has_legal_moves()
            return model.game_state
        elif msg_name == "has_surrounding_empty_tile":
            model.has_surrounding_empty_tile(msg[1], msg[2])
            return model.game_state
        elif msg_name == "is_board_full":
            model.is_board_full()
            return model.game_state
        elif msg_name == "change_turn":
            model.change_turn()
            return model.game_state
        elif msg_name == "get_winner":
            return model.get_winner()
        elif msg_name == "get_leaderboard":
            model.get_leaderboard()
            return model.game_state
        elif msg_name == "get_to_JSON":
            return model.to_JSON()
        elif msg_name == "get_from_JSON":
            model.from_JSON()
            return model.game_state
        elif msg_name == "update_active_game":
            model.update_active_game(self.ActiveGamesManager)
            return model.game_state
        elif msg_name == "add_game_to_active_games":
            model.add_game_to_active_games(self.ActiveGamesManager)
            return model.game_state
        elif msg_name == "get_player":
            return model.get_player(msg[1])
        elif msg_name == "set_player_elo":
            model.set_player_elo()
            return model.game_state
        elif msg_name == "update_elo":
            model.update_elo(msg[1])
            return model.game_state
        elif msg_name == "get_online_players":
            # FIXME This will break
            return self.get_active_players()
        elif msg_name == "add_active_player":
            self.add_active_player(msg[1])
            return model.game_state
        elif msg_name == "add_online_session":
            self.add_online_session(msg[1], msg[2], address)
            return model.game_state
        elif msg_name == "accept_session":
            self.accept_session(msg[1], address)
            return model.game_state
        return None

    def get_active_players(self):
        return self.db.get_activePlayer()

    def add_active_player(self, username):
        self.db.addActivePlayer(username)

    def add_online_session(self, username1, username2, address):
        username2 = username2[2:-3]
        self.online_sessions[(username1, username2)] = self.models[address]
        self.address_to_session[address] = (username1, username2)

    def accept_session(self, username, address):
        keys = self.online_sessions.keys()
        for key in keys:
            if username in key:
                self.address_to_session[address] = key
                break


if __name__ == "__main__":
    server = Server()
    server.start()
