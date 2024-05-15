import asyncio
import tkinter as tk
from tkinter import ttk

import bashorg_parser


class App:
    async def exec(self) -> None:
        self.window = MainWindow(asyncio.get_event_loop())
        await self.window.show_window()


class MainWindow(tk.Tk):
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        print(type(self.loop))
        self.root = tk.Tk()
        self.exit_flag = False
        self.set_up_window()

    def set_up_window(self) -> None:
        self.root.title("Цитаты Баша")
        self.root.geometry("600x600")
        self.root.maxsize(600, 600)
        self.root.minsize(600, 600)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.info_label1 = ttk.Label(text="Показать Цитаты:", font="Arial 12")
        self.info_label2 = ttk.Label(text="Количество:", font="Arial 12")
        self.entry_num_of_quotes = tk.Entry()
        self.entry_num_of_quotes.insert(0, "10")
        self.text_place = tk.Text()
        self.text_scroll = tk.Scrollbar(command=self.text_place.yview)
        self.text_place.config(yscrollcommand=self.text_scroll.set)
        self.text_place.config(state=tk.DISABLED)

        self.btn_best_quotes = ttk.Button(
            text="Лучшие", width=35, command=lambda: self.loop.create_task(self.show_best_quotes())
        )
        self.btn_random_quotes = ttk.Button(
            text="Случайные", width=35, command=lambda: self.loop.create_task(self.show_random_quotes())
        )
        self.btn_latest_quotes = ttk.Button(
            text="Последние", width=35, command=lambda: self.loop.create_task(self.show_latest_quotes())
        )

        self.text_scroll.place(x=576, y=20, height=550)
        self.info_label1.place(x=20, y=20)
        self.info_label2.place(x=20, y=60)
        self.entry_num_of_quotes.place(x=120, y=60)
        self.btn_best_quotes.place(x=20, y=100, height=70)
        self.btn_random_quotes.place(x=20, y=270, height=70)
        self.btn_latest_quotes.place(x=20, y=440, height=70)
        self.text_place.place(x=300, y=20, height=550, width=275)

    async def show_window(self) -> None:
        while not self.exit_flag:
            self.root.update()
            await asyncio.sleep(0)

    async def show_best_quotes(self) -> None:
        self.text_place.config(state=tk.NORMAL)
        self.text_place.delete("0.0", tk.END)
        if not self.entry_num_of_quotes.get().isdigit():
            self.entry_num_of_quotes.delete(0, tk.END)
            self.entry_num_of_quotes.insert(0, "10")
        quotes = await bashorg_parser.get_best_quotes(int(self.entry_num_of_quotes.get()))
        quotes.reverse()
        for i in range(len(quotes)):
            quote = f"\n\n--------\n" + quotes[i] + "\n---------\n\n"
            self.text_place.insert(f"{i}.0", quote)
        self.text_place.config(state=tk.DISABLED)

    async def show_random_quotes(self) -> None:
        self.text_place.config(state=tk.NORMAL)
        self.text_place.delete("0.0", tk.END)
        if not self.entry_num_of_quotes.get().isdigit():
            self.entry_num_of_quotes.delete(0, tk.END)
            self.entry_num_of_quotes.insert(0, "10")
        quotes = await bashorg_parser.get_random_quotes(int(self.entry_num_of_quotes.get()))
        quotes.reverse()
        for i in range(len(quotes)):
            quote = "\n\n---------\n" + quotes[i] + "\n---------\n\n"
            self.text_place.insert(f"{i}.0", quote)
        self.text_place.config(state=tk.DISABLED)

    async def show_latest_quotes(self) -> None:
        self.text_place.config(state=tk.NORMAL)
        self.text_place.delete("0.0", tk.END)
        if not self.entry_num_of_quotes.get().isdigit():
            self.entry_num_of_quotes.delete(0, tk.END)
            self.entry_num_of_quotes.insert(0, "10")
        quotes = await bashorg_parser.get_latest_quotes(int(self.entry_num_of_quotes.get()))
        quotes.reverse()
        for i in range(len(quotes)):
            quote = "\n\n---------\n" + quotes[i] + "\n---------\n\n"
            self.text_place.insert(f"{i}.0", quote)
        self.text_place.config(state=tk.DISABLED)

    def on_closing(self) -> None:
        self.root.destroy()
        self.exit_flag = True


if __name__ == "__main__":
    app = App()
    asyncio.run(app.exec())
