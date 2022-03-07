import tkinter as tk
import tkinter.messagebox
from tkinter import messagebox
from typing import overload

from controller.local_controller import LocalController
from model.model import Game
from model.player import player_symbol, Player
from view.game_view import GameView
# from tkinter import OptionMenu


class GUIView(tk.Tk):
    def __init__(self, game_controller: LocalController, board):
        self.game_controller = game_controller
        tk.Tk.__init__(self)
        self.board = board
        self.title("Reversi")
        self.container = tk.Frame(self, width=(75 * 8), height=(75 * 9))
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage, SettingsPage, PlayPage, LeaderboardPage):
            page_name = F.__name__
            # print(F.__class__)
            #frame = F(parent=self.container, controller=self)
            if F == PlayPage:
                self.game_controller.change_board_size(8)
                frame = F(parent=self.container, controller=self, board=self.board)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame = F(parent=self.container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")

        self.change_page("LoginPage")

    '''
    def set_controller(self, game_controller):
        self.game_controller = game_controller
    '''
    def change_page(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "PlayPage":
            frame.start_game()
            frame.display_board()
            # self.frames[page_name].board_size
            # self.frames[page_name] = PlayPage()
            # self.game_controller.run_game()
            # self.game_controller.run_game()

    def change_board_size(self, size):
        self.frames["PlayPage"] = PlayPage(parent=self.container, controller=self, board_size=size)
        self.frames["PlayPage"].grid(row=0, column=0, sticky="nsew")
        self.change_page("SettingsPage")


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
                                 command=lambda: controller.change_page("MainPage"))
        guest_button.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main Page")
        label.pack(side="top", pady=10)
        play_button = tk.Button(self, text="Play Game",
                                command=lambda: controller.change_page("PlayPage"))
        settings_button = tk.Button(self, text="Settings",
                                    command=lambda: controller.change_page("SettingsPage"))
        leaderboard_button = tk.Button(self, text="View Leaderboard",
                                       command=lambda: controller.change_page("LeaderboardPage"))
        load_crashed_game_button = tk.Button(self, text="Load Crashed Game")
        play_button.pack(pady=5)
        settings_button.pack(pady=5)
        leaderboard_button.pack(pady=5)
        load_crashed_game_button.pack(side="bottom", pady=10)


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
                                  command=lambda: controller.change_page("MainPage"))
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
    def __init__(self, parent, controller, board=None):
        tk.Frame.__init__(self, parent)
        GameView.__init__(self, board, controller.game_controller)
        self.parent = parent
        self.controller = controller
        self.board = board
        self.board_size = board.shape[0]
        self.buttons = [[0 for x in range(self.board_size)] for y in range(self.board_size)]
        exit_button = tk.Button(self, text="Exit Game",
                                command=lambda: self.display_exit())
        self.invalid_move_label = tk.Label(self, text="Invalid move. Try again.", fg="red")
        # label = tk.Label(self, text="Play")
        # label.pack(side="top", pady=10)
        for i in range(self.board_size):
            self.rowconfigure(i, minsize=60)
            self.columnconfigure(i, minsize=60)
        self.set_buttons()
        exit_button.grid(row=self.board_size+1, column=self.board_size-1, sticky="nsew")

    def display_board(self):
        self.invalid_move_label.grid_forget()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == Player.X and self.buttons[i][j].cget('bg') != player_symbol[self.board[i][j]]:
                    self.buttons[i][j].configure(bg="black")
                    self.buttons[i][j].configure(command=None)
                elif self.board[i][j] == Player.O and self.buttons[i][j].cget('bg') != player_symbol[self.board[i][j]]:
                    self.buttons[i][j].configure(bg="white")
                    # slightly worse performance to call this on every color change
                    self.buttons[i][j].configure(command=None)
        self.update()

    def set_buttons(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                # command=lambda arg=(i, j): self.button_clicked(arg)
                button = 0
                self.buttons.append(button)
                self.buttons[i][j] = tk.Button(self, text=f'({i},{j})', bg="green",
                                   command=lambda i=i, j=j:
                                   self.request_move(i, j))
                self.buttons[i][j].grid(row=i, column=j, sticky='nsew')

    def display_curr_player(self, player):
        curr_player = tk.Label(self, text=f'Current Player:{player}')
        curr_player.grid(row=self.board_size+1)

    def display_winner(self, winner):
        messagebox.showinfo("Congratulations!", f'Player {winner} has won! Congratulations!')
        self.controller.change_page("MainPage")

    def display_illegal_move(self):
        self.invalid_move_label.grid(row=self.board_size+1, column=self.board_size-5)

    def display_no_legal_moves(self, player):
        messagebox.showerror("No Legal Moves", "No Legal Moves - Other Player's Turn")

    # rename to make move
    def request_move(self, i, j):
        i = i
        j = j
        self.controller.game_controller.play_turn(i, j)
        # return f'{i},{j}'

    def start_game(self):
        self.controller.game_controller.reset_game()
        self.board = self.controller.game_controller.model.board
        self.set_buttons()
        self.display_curr_player(Player.X)

    def display_exit(self):
        messagebox.showinfo("Exiting", "Exiting Game - Returning to Main Menu")
        self.controller.change_page("MainPage")


class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Leaderboard")
        label.pack(side="top", pady=10)
        main_button = tk.Button(self, text="Return to Main page",
                                command=lambda: controller.change_page("MainPage"))
        players = tk.Label(self, text="No players currently on leaderboard", font=14)
        players.pack(padx=10,pady=10)
        main_button.pack(pady=10)


if __name__ == "__main__":
    game = Game()

    controller = LocalController(game)
    game_view = GUIView(controller, game.board)
    controller.set_view(game_view.frames["PlayPage"])

    # game_view.set_controller(controller)

    while(True):
        game_view.update()
        # controller.run_game()
