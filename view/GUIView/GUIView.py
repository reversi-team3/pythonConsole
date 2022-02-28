import tkinter as tk
import tkinter.messagebox

from controller.local_controller import LocalController
from model.model import Game
from view.game_view import GameView
# from tkinter import OptionMenu


class GUIView(tk.Tk):
    def __init__(self, game_controller):
        self.game_controller = game_controller
        tk.Tk.__init__(self)
        self.title("Reversi")
        self.container = tk.Frame(self, width=(75 * 8), height=(75 * 9))
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage, SettingsPage, PlayPage, LeaderboardPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def set_controller(self, game_controller):
        self.game_controller = game_controller

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.lift()

    def change_board_size(self, size):
        self.frames["PlayPage"] = PlayPage(parent=self.container, controller=self, board_size=size)
        self.frames["PlayPage"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("SettingsPage")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # username
        username_label = tk.Label(self, text='Username:')
        username_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        username_entry = tk.Entry(self)
        username_entry.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)
        # password
        password_label = tk.Label(self, text='Password:')
        password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        password_entry = tk.Entry(self, show='*')
        password_entry.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)
        # login button
        login_button = tk.Button(self, text='Login', width=10)
        login_button.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)

        guest_button = tk.Button(self, text='Play as Guest', width=10,
                                 command=lambda: controller.show_frame("MainPage"))
        guest_button.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main Page")
        label.pack(side="top", pady=10)
        play_button = tk.Button(self, text="Play Game",
                                command=lambda: controller.show_frame("PlayPage"))
        settings_button = tk.Button(self, text="Settings",
                                    command=lambda: controller.show_frame("SettingsPage"))
        leaderboard_button = tk.Button(self, text="View Leaderboard",
                                       command=lambda: controller.show_frame("LeaderboardPage"))
        play_button.pack()
        settings_button.pack()
        leaderboard_button.pack()


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Settings")
        label.pack(side="top", pady=10)
        options = [
            6,
            8,
            10
        ]
        self.options_type = tk.StringVar()
        self.options_type.set(options[1])
        drop_down = tk.OptionMenu(self, self.options_type, *options)
        drop_down_label = tk.Label(self, text="Board size")
        confirm_button = tk.Button(self, text="Confirm",
                                   command=self.confirm_size)
        return_button = tk.Button(self, text="Return",
                                  command=lambda: controller.show_frame("MainPage"))
        drop_down_label.pack()
        drop_down.pack()
        confirm_button.pack(pady=5)
        return_button.pack(pady=5)

    def confirm_size(self):
        if int(self.options_type.get()) != self.controller.game_controller.model.board.size:
            self.controller.game_controller.change_board_size(int(self.options_type.get()))
            self.controller.change_board_size(int(self.options_type.get()))
            tkinter.messagebox.showinfo(title="Success", message="Board size updated")


class PlayPage(tk.Frame, GameView):
    def __init__(self, parent, controller, board_size=8):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="Play")
        # label.pack(side="top", pady=10)
        exit_button = tk.Button(self, text="Exit Game",
                                command=lambda: controller.show_frame("MainPage"))

        for i in range(board_size):
            self.rowconfigure(i, minsize=60)
            self.columnconfigure(i, minsize=60)
        for i in range(board_size):
            for j in range(board_size):
                # command=lambda arg=(i, j): self.button_clicked(arg)
                button = tk.Button(self, text=f'({i},{j})',)
                button.grid(row=i, column=j, sticky='nsew')
        # exit_button.pack()

    def display_board(self):
        pass

    def display_curr_player(self, player):
        pass

    def display_winner(self, winner):
        pass

    def display_illegal_move(self):
        pass

    def display_no_legal_moves(self, player):
        pass

    def get_move(self):
        pass

    def display_exit(self):
        pass

    def request_move(self):
        pass


class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Leaderboard")
        label.pack(side="top", pady=10)
        main_button = tk.Button(self, text="Return to Main page",
                                command=lambda: controller.show_frame("MainPage"))
        players = tk.Label(self, text="No players currently on leaderboard", font=14)
        players.pack(padx=10,pady=10)
        main_button.pack(pady=10)


if __name__ == "__main__":
    game = Game()

    controller = LocalController(game)
    game_view = GUIView(controller)

    game_view.set_controller(controller)

    game_view.mainloop()
