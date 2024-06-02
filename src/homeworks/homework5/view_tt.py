from tkinter import BOTH, LEFT, YES, ttk
from typing import Any


class MainView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, font=("Arial", 14), text="Welcome to TicTacToe\nSelect mode:")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        combobox_values = ("Easy bot", "Hard bot", "One computer", "Connect to game", "Create the game")
        self.select_gamemode = ttk.Combobox(self, values=combobox_values, state="readonly")
        self.select_gamemode.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.select_gamemode.bind("<<ComboboxSelected>>", self.gamemode_chosen)

        self.side_label = ttk.Label(self, font=("Arial", 14), text="Select side:")
        self.side_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.side = ttk.Combobox(
            self,
            values=("X", "0"),
            state="readonly",
        )
        self.side.set("X")
        self.side.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.ip_label = ttk.Label(self, font=("Arial", 14), text="Enter ip:")

        self.ip_input = ttk.Entry(self)
        self.ip_input.insert(0, "192.168.0.1")

        self.btn = ttk.Button(self, text="Start game")

    def gamemode_chosen(self, event: Any) -> None:
        value = self.select_gamemode.get()
        if value in ["Easy bot", "Hard bot", "One computer"]:
            self.btn.grid_forget()
            self.ip_label.grid_forget()
            self.ip_input.grid_forget()
            self.btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        else:
            self.btn.grid_forget()
            self.ip_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
            self.ip_input.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
            self.btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


class GameFieldView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.lines = []
        self.game_btns: list[list[ttk.Button]] = [[], [], []]

        for i in range(3):
            self.lines.append(ttk.Frame(self))
            self.lines[i].pack()
            for j in range(3):
                self.game_btns[i].append(ttk.Button(self.lines[i], text="\n\n\n"))
                self.game_btns[i][j].pack(expand=YES, fill=BOTH, side=LEFT)


class GameView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.curr_turn_label = ttk.Label(self, text="", font=("Arial", 20))
        self.curr_turn_label.grid(row=0, columnspan=2, padx=10, pady=10)
        self.field_view = GameFieldView()
        self.field_view.grid(row=0, column=0)
        self.btn_quit = ttk.Button(self, text="Quit")
