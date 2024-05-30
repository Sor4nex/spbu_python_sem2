import abc
from tkinter import Tk, ttk
from typing import Optional, Callable

from model_tt import TicTacToe, Player
from view_tt import GameView, MainView, ResultView


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: TicTacToe):
        self._model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, model: TicTacToe, root: Tk):
        self._model = model
        self._root = root

        self._viewmodels: dict[str, IViewModel] = {
            "main": MainViewModel(self._model),
            "game": GameViewModel(self._model),
            "result": ResultViewModel(self._model),
        }

        self._session_callback_rm = model.add_session_listener(self._session_observer)
        self._current_view: Optional[ttk.Frame] = None

    def _session_observer(self, mode: Optional[str]):
        if mode is None:
            self.switch("main", {})
        elif mode == "game":
            self.switch("game", {"user": self._model.players["player1"]})
        elif mode == "result":
            winner = "Player 1" if self._model.current_turn.value == self._model.players["player1"] else "Player 2"
            self.switch("result", {"winner": winner})
        else:
            raise RuntimeError("Unknown state of application")

    def switch(self, name: str, data: dict):
        if name not in self._viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")
        if self._current_view is not None:
            self._current_view.destroy()
        self._current_view = self._viewmodels[name].start(self._root, data)
        self._current_view.grid(row=0, column=0, sticky="NSEW")

    def start(self):
        self.switch("main", {})


class MainViewModel(IViewModel):
    def _bind(self, view: MainView):
        view.btn.config(command=lambda: self._model.start_game("bot", True))

    def start(self, root: Tk, data: dict):
        frame = MainView(root)
        self._bind(frame)
        return frame


class GameViewModel(IViewModel):
    def __init__(self, model: TicTacToe) -> None:
        self.user: Optional[Player] = None
        self._turn_callback_rm: Optional[Callable] = None
        super().__init__(model)

    def _bind(self, view: GameView) -> None:
        turn = "player 1" if self.user.my_turn else "player2"
        view.curr_turn_label.config(text=f"now turn {turn}")
        for i in range(3):
            for j in range(3):
                com = lambda x=i, y=j: self.user.make_turn((x, y))
                view.field_view.game_btns[i][j].config(command=com)

        def _destroy_wrapper(original_destroy):
            def destroy():
                original_destroy()
                self._turn_callback_rm()

            return destroy

        view.destroy = _destroy_wrapper(view.destroy)

    def update_game_view(self, view, my_turn: Optional[bool]) -> None:
        if my_turn is None:
            pass
            # блокируем кнопки
            # красиво пишем что выиграл тот то игрок выйти в меню
        turn = "player 1" if my_turn else "player2"
        view.header.config(text=f"now turn {turn}")
        view.update()

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        self.user = data["user"]
        frame = GameView(root)
        self._bind(frame)
        self._turn_callback_rm: Callable = self.user.add_turn_listener(lambda x: self.update_game_view(frame, x))
        return frame


class ResultViewModel(IViewModel):
    def __init__(self, model: TicTacToe) -> None:
        self.winner: Optional[str] = None
        super().__init__(model)

    def _bind(self, view: ResultView) -> None:
        view.header.config(text=f"выиграл {self.winner}")
        view.btn.config(command=lambda: self._model.end_game())

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = ResultView(root)
        self.winner = data["winner"]
        self._bind(frame)
        return frame
