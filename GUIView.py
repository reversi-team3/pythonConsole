import time
import tkinter as tk
import tkinter.messagebox
from tkinter import messagebox

from controller.controller_new import NewController
from model.ai_player import AIPlayer
from model.game_model import Game
from model.online_player import OnlinePlayer
from model.player import Color
from view.game_view import GameView


# from tkinter import OptionMenu


class GUIView(tk.Tk):
    def __init__(self, game_controller: NewController, board):
        self.game_controller = game_controller
        tk.Tk.__init__(self)
        self.board = board
        self.title("Reversi")
        self.container = tk.Frame(self, width=(75 * 8), height=(75 * 9))
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage, SettingsPage, PlayPage, GameModePage, RegisterPage):
            page_name = F.__name__
            # print(F.__class__)
            # frame = F(parent=self.container, controller=self)
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
        self.frames["PlayPage"] = PlayPage(parent=self.container, controller=self,
                                           board=self.game_controller.model.board)
        self.frames["PlayPage"].grid(row=0, column=0, sticky="nsew")
        self.game_controller.set_view(game_view.frames["PlayPage"])
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
        login_button = tk.Button(self, text='Login', width=10,
                                 command=lambda: [self.login_verify(username_entry.get(), password_entry.get())])
        login_button.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)

        guest_button = tk.Button(self, text='Play as Guest', width=10,
                                 command=lambda: self.guest_play())
        guest_button.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        register_button = tk.Button(self, text='Sign Up', width=20,
                                    command=lambda: controller.change_page("RegisterPage"))
        register_button.grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)

    def guest_play(self):
        self.controller.game_controller.model.player_one = OnlinePlayer("Guest", Color.BLACK)
        self.controller.change_page("MainPage")

    def login_verify(self, username, password):
        rows = db.checkPlayer(username)
        playerExist = len(rows)
        for row in rows:
            pw1 = row[0]

        if playerExist:
            if pw1 == password:
                self.login_sucess(username)
            else:
                self.password_not_recognised()

        else:
            self.user_not_found()

    def login_sucess(self, username):
        global login_success_screen
        login_success_screen = tk.Tk()
        login_success_screen.title("Success")
        login_success_screen.geometry("150x100")
        tk.Label(login_success_screen, text="Login Success").pack()
        tk.Button(login_success_screen, text="OK",
                  command=self.delete_login_success).pack()
        self.controller.game_controller.model.player_one = OnlinePlayer(username, Color.BLACK)

    def password_not_recognised(self):
        global password_not_recog_screen
        password_not_recog_screen = tk.Tk()
        password_not_recog_screen.title("Success")
        password_not_recog_screen.geometry("150x100")
        tk.Label(password_not_recog_screen, text="Invalid Password ").pack()
        tk.Button(password_not_recog_screen, text="OK",
                  command=self.delete_password_not_recognised).pack()

    def user_not_found(self):
        global user_not_found_screen
        user_not_found_screen = tk.Tk()
        user_not_found_screen.title("Success")
        user_not_found_screen.geometry("150x100")
        tk.Label(user_not_found_screen, text="User Not Found").pack()
        tk.Button(user_not_found_screen, text="OK",
                  command=self.delete_user_not_found_screen).pack()

    # Deleting popups

    def delete_login_success(self):
        login_success_screen.destroy()
        self.controller.change_page("MainPage")

    def delete_password_not_recognised(self):
        password_not_recog_screen.destroy()

    def delete_user_not_found_screen(self):
        user_not_found_screen.destroy()


class RegisterPage(tk.Frame):
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

        register_button = tk.Button(self, text='Register Account', width=15,
                                    command=lambda: [self.write_File(username_entry.get(), password_entry.get()),
                                                     self.clear_cells(username_entry, password_entry)])
        register_button.grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)

        back_button = tk.Button(self, text='Back to Login', width=20,
                                command=lambda: controller.change_page("LoginPage"))

        back_button.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

    def write_File(self, username_input, password_input):
        # registration_label = tk.Label(self, text = '')
        # registration_label.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        # error_label = tk.Label(self, text = '')
        # error_label.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        try:
            if username_input != '' and password_input != '':
                # blank_label = tk.Label(self, text = '                                 ')
                # blank_label.grid(row = 5, column=1, sticky=tk.W, padx=5, pady=5)
                # with open('Registration.txt', 'a') as file:
                #     file.write(username_input + "\n")
                #     file.write(password_input + "\n" + "\n")
                #     file.close()
                #     print ("Successful")
                db.addPlayer(username_input, password_input)

                registration_label = tk.Label(self, text='         Registration Success                      ',
                                              fg='green')
                registration_label.grid(row=5, column=1, sticky=tk.W, padx=20, pady=5)
            else:
                error_label = tk.Label(self, text='    Username/Password cannot be blank', fg='red')
                error_label.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
                # error_label.after(1000, error_label.destroy())
        except:
            self.failed_reg()

    def failed_reg(self):
        global failed_reg_screen
        failed_reg_screen = tk.Tk()
        failed_reg_screen.title("Success")
        failed_reg_screen.geometry("150x100")
        tk.Label(failed_reg_screen, text="Duplicated Username").pack()
        tk.Button(failed_reg_screen, text="OK",
                  command=self.delete_failed_reg).pack()

    def delete_failed_reg(self):
        failed_reg_screen.destroy()

    def remove_label(self, label):
        label.config(text="")

    def clear_cells(self, username, password):
        username.delete(0, tk.END)
        password.delete(0, tk.END)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Main Page")
        label.pack(side="top", pady=10)
        play_button = tk.Button(self, text="Play Game",
                                command=lambda: controller.change_page("GameModePage"))
        settings_button = tk.Button(self, text="Settings",
                                    command=lambda: controller.change_page("SettingsPage"))
        leaderboard_button = tk.Button(self, text="View Leaderboard",
                                       command=lambda: controller.change_page("LeaderboardPage"))
        login_page_button = tk.Button(self, text="Sign out",
                                      command=lambda: self.sign_out())
        exit_button = tk.Button(self, text="Exit",
                                command=lambda: self.close())
        load_crashed_game_button = tk.Button(self, text="Load Crashed Game")
        play_button.pack(pady=5)
        settings_button.pack(pady=5)
        leaderboard_button.pack(pady=5)
        login_page_button.pack(pady=5)
        exit_button.pack(pady=5)
        load_crashed_game_button.pack(side="bottom", pady=10)

    def close(self):
        sign_out_message = messagebox.askquestion("Exiting", "Are you sure you want to exit the application?")
        if sign_out_message == 'yes':
            self.controller.destroy()

    def sign_out(self):
        sign_out_message = messagebox.askquestion("Signing out", "Are you sure you want to sign out?")
        if sign_out_message == 'yes':
            self.controller.change_page("LoginPage")


class GameModePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        label = tk.Label(self, text="Select game mode")
        options = [
            "Easy",
            "Medium",
            "Hard"
        ]
        self.options_type = tk.StringVar()
        self.options_type.set(options[0])
        drop_down = tk.OptionMenu(self, self.options_type, *options)
        drop_down_label = tk.Label(self, text="AI Difficulty")
        label.pack(side="top", pady=10)
        ai_button = tk.Button(self, text="AI Mode",
                              command=lambda: self.set_mode('ai'))
        local_button = tk.Button(self, text="Local Mode", command=lambda: self.set_mode('local'))
        online_button = tk.Button(self, text="Online Mode", command=lambda: self.set_mode('online'))
        drop_down_label.pack()
        drop_down.pack()
        ai_button.pack(pady=5)
        local_button.pack(pady=5)
        online_button.pack(pady=5)

    def set_mode(self, mode):
        if mode == 'ai':
            self.controller.game_controller.model.player_two = AIPlayer(self.controller.game_controller.model)
            self.controller.game_controller.model.player_two.change_difficulty(self.options_type.get())
        self.controller.game_controller.set_view(self.controller.frames["PlayPage"])
        self.controller.change_page("PlayPage")


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
        colors = [
            "red",
            "blue",
            "black",
            "purple"
        ]
        self.options_type = tk.StringVar()
        self.options_type.set(options[1])
        drop_down = tk.OptionMenu(self, self.options_type, *options)
        drop_down_label = tk.Label(self, text="Board size")
        confirm_button = tk.Button(self, text="Confirm",
                                   command=self.confirm_size)
        return_button = tk.Button(self, text="Return",
                                  command=lambda: controller.change_page("MainPage"))
        self.colors_type = tk.StringVar()
        self.colors_type.set(options[2])
        colors_drop_down = tk.OptionMenu(self, self.colors_type, *colors)
        colors_label = tk.Label(self, text="Disk Color")
        colors_confirm = tk.Button(self, text="Confirm Color", command=self.confirm_color)
        drop_down_label.pack()
        drop_down.pack()
        confirm_button.pack(pady=5)
        colors_label.pack()
        colors_drop_down.pack()
        colors_confirm.pack()
        return_button.pack(pady=5)

    def confirm_color(self):
        self.controller.game_controller.model.player_one.change_color(self.colors_type.get())
        tkinter.messagebox.showinfo(title="Success", message="Disk color updated")

    def confirm_size(self):
        if int(self.options_type.get()) != self.controller.game_controller.model.board.shape[0]:
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
        self.invalid_move_label = tk.Label(self, text="Invalid move.\nTry again.", fg="red")
        for i in range(self.board_size):
            self.rowconfigure(i, minsize=60)
            self.columnconfigure(i, minsize=60)
        self.set_buttons()
        exit_button.grid(row=self.board_size + 1, column=0, sticky="nsew")

    def display_board(self):
        player_one = self.controller.game_controller.model.player_one
        player_two = self.controller.game_controller.model.player_two
        self.invalid_move_label.grid_forget()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == player_one and \
                        self.buttons[i][j].cget('bg') != self.board[i][j].color.value:
                    self.buttons[i][j].configure(bg=player_one.color.value)
                    self.buttons[i][j].configure(command=None)
                elif self.board[i][j] == player_two and self.buttons[i][j].cget('bg') != self.board[i][j].color.value:
                    self.buttons[i][j].configure(bg=player_two.color.value)
                    # slightly worse performance to call this on every color change
                    self.buttons[i][j].configure(command=None)
        self.update()

    def set_buttons(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                # command=lambda arg=(i, j): self.button_clicked(arg)
                button = 0
                self.buttons.append(button)
                self.buttons[i][j] = tk.Button(self, bg="green",
                                               command=lambda i=i, j=j:
                                               self.request_move(i, j))
                self.buttons[i][j].grid(row=i, column=j, sticky='nsew')

    def display_curr_player(self, player):
        curr_player = tk.Label(self, text=f'Current Player:{player.username}')
        curr_player.grid(row=self.board_size + 1, column=self.board_size + 1)

    def display_winner(self, winner):
        messagebox.showinfo("Congratulations!", f'Player {winner} has won! Congratulations!')
        self.controller.change_page("MainPage")

    def display_illegal_move(self):
        self.invalid_move_label.grid(row=self.board_size - 1, column=self.board_size + 1)

    def display_no_legal_moves(self, player):
        messagebox.showerror("No Legal Moves", "No Legal Moves - Other Player's Turn")

    # rename to make move
    def request_move(self, i, j):
        move = self.controller.game_controller.model.curr_player.receive_move(i, j)
        self.controller.game_controller.play_turn(move[0], move[1])
        if isinstance(self.controller.game_controller.model.curr_player, AIPlayer):
            time.sleep(.75)
            move2 = self.controller.game_controller.model.curr_player.receive_move(i, j)
            self.controller.game_controller.play_turn(move2[0], move2[1])

        # return f'{i},{j}'

    def start_game(self):
        self.controller.game_controller.reset_game()
        self.board = self.controller.game_controller.model.board
        self.set_buttons()
        self.display_curr_player(self.controller.game_controller.model.player_one)

    def display_exit(self):
        exit_message = messagebox.askquestion("Exiting", "Are you sure you want to exit?")
        if (exit_message == 'yes'):
            self.controller.change_page("MainPage")


class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Leaderboard")
        label.pack(side="top", pady=10)
        main_button = tk.Button(self, text="Return to Main page",
                                command=lambda: controller.change_page("MainPage"))
        main_button.pack(pady=10)

        # rows = db.checkRank()

        # for i, name in enumerate(rows):
        #     db.updateLeaderboard(name,i+1)

        # leaderboard = db.getLeaderboard()
        # users = self.controller.game_controller.get_leaderboard()
        for x in rows:
            tk.Label(self, text=x).pack(pady=5)


if __name__ == "__main__":
    game = Game()
    # db = DBManager.get_instance()
    controller = NewController(game)
    game_view = GUIView(controller, game.board)
    controller.set_view(game_view.frames["PlayPage"])

    # game_view.set_controller(controller)

    game_view.mainloop()
