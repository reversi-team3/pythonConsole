import tkinter as tk


class GUIView(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self, width=(75 * 8), height=(75 * 9))
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage, SettingsPage, PlayPage, LeaderboardPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


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
        confirm_button = tk.Button(self, text="Confirm")
        return_button = tk.Button(self, text="Return",
                                  command=lambda: controller.show_frame("MainPage"))
        confirm_button.pack()
        return_button.pack()


class PlayPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="Play")
        # label.pack(side="top", pady=10)
        exit_button = tk.Button(self, text="Exit Game",
                                command=lambda: controller.show_frame("MainPage"))
        for i in range(8):
            self.rowconfigure(i, minsize=75)
            self.columnconfigure(i, minsize=75)
        for i in range(8):
            for j in range(8):
                # command=lambda arg=(i, j): self.button_clicked(arg)
                button = tk.Button(self, text=f'({i},{j})',)
                button.grid(row=i, column=j, sticky='nsew')
        # exit_button.pack()


class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Leaderboard")
        label.pack(side="top", pady=10)
        main_button = tk.Button(self, text="Return to Main page",
                                command=lambda: controller.show_frame("MainPage"))
        main_button.pack()


if __name__ == "__main__":
    game = GUIView()
    game.mainloop()
