from tkinter import ttk


class MainView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="HALOW")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.btn = ttk.Button(self, text="Поздняков.Подписаться")
        self.btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


class GameView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.btn = ttk.Button(self, text="ХРЫЫ")
        self.btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.btn1 = ttk.Button(self, text="win")
        self.btn2 = ttk.Button(self, text="change player")
        self.btn1.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.btn2.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


class ResultView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text="")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.btn = ttk.Button(self, text="квит баляд")
        self.btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
