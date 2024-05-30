from tkinter import ttk, BOTH, YES, LEFT
from typing import Any


class MainView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="HALOW")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.btn = ttk.Button(self, text="Поздняков.Подписаться")
        self.btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.curr_turn_label = ttk.Label(self, text="")
        self.curr_turn_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.field_view = GameFieldView()
        self.field_view.grid(row=0, column=0)
        self.btn_quit = ttk.Button(self, text="Quit")


class ResultView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.btn = ttk.Button(self, text="квит баляд")
        self.btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
