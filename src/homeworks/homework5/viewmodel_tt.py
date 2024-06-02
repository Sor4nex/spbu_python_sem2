import abc
from tkinter import Tk, ttk
from typing import Callable, Optional

from src.homeworks.homework5.model_tt import Player, TicTacToe, UserPlayer
from src.homeworks.homework5.view_tt import GameFieldView, GameView, MainView


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: TicTacToe) -> None:
        self._model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: dict) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, model: TicTacToe, root: Tk) -> None:
        self._model = model
        self._root = root

        self._viewmodels: dict[str, IViewModel] = {
            "main": MainViewModel(self._model),
            "game": GameViewModel(self._model),
        }

        self._session_callback_rm = model.add_session_listener(self._session_observer)
        self._current_view: Optional[ttk.Frame] = None

    def _session_observer(self, mode: Optional[str], additional: dict) -> None:
        if mode is None:
            self.switch("main", {})
        elif mode == "game":
            self.switch(
                "game", {"player 1": self._model.players["player1"], "player 2": self._model.players["player2"]}
            )
        else:
            raise RuntimeError("Unknown state of application")

    def switch(self, name: str, data: dict) -> None:
        if name not in self._viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")
        if self._current_view is not None:
            self._current_view.destroy()
        self._current_view = self._viewmodels[name].start(self._root, data)
        self._current_view.grid(row=0, column=0, sticky="NSEW")

    def start(self) -> None:
        self.switch("main", {})


class MainViewModel(IViewModel):
    def _bind(self, view: MainView) -> None:
        view.btn.config(command=lambda: self.get_info_to_start(view))

    def get_info_to_start(self, view: MainView) -> None:
        gamemode = view.select_gamemode.get()
        side = view.side.get() == "X"
        ip = view.ip_input.get()
        self._model.start_game(gamemode, side, ip)

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        frame = MainView(root)
        self._bind(frame)
        return frame


class GameViewModel(IViewModel):
    def __init__(self, model: TicTacToe) -> None:
        self.opponent: Optional[Player] = None
        super().__init__(model)

    def _bind(self, view: GameView) -> None:
        if self.user is not None:
            turn = "player 1" if self.user.my_turn.value else "player2"
        view.curr_turn_label.config(text=f"now turn {turn}")
        view.btn_quit.config(command=lambda: self._model.end_game())
        for i in range(3):
            for j in range(3):
                com = lambda x=i, y=j: self.make_player_turn((x, y))
                view.field_view.game_btns[i][j].config(command=com)

        def _destroy_wrapper(original_destroy: Callable) -> Callable:
            def destroy() -> None:
                original_destroy()
                self._turn_callback_rm()

            return destroy

        setattr(view, "destroy", _destroy_wrapper(view.destroy))

    def make_player_turn(self, coords: tuple[int, int]) -> None:
        if self.user.my_turn.value:
            self._model.make_turn(self.user, coords)
        elif self.opponent is not None:
            self._model.make_turn(self.opponent, coords)

    def update_game_view(self, view: GameView, my_turn: Optional[bool], additional: dict) -> None:
        if self.user is None:
            return
        self.update_field(view.field_view)
        if my_turn is None:
            return self.update_win(view, additional)
        if my_turn:
            view.curr_turn_label.config(text=f"Now turn Player 1 ({self.user.side})")
            self._unblock_btns(view.field_view)
        else:
            side = "X" if self.user.side == "0" else "0"
            view.curr_turn_label.config(text=f"Now turn Player 2 ({side})")
            if self.opponent is None:
                self._block_btns(view.field_view)
        view.update()

    def update_win(self, view: GameView, info: dict) -> None:
        self._block_btns(view.field_view)
        view.btn_quit.grid(row=1, columnspan=2, padx=10, pady=10)
        winner = info.get("winner", None)
        if winner is None:
            winner_txt = "Draw!"
        elif winner is self.user:
            winner_txt = f"Player 1 wins! ({self.user.side})"
        else:
            side = "X" if self.user.side == "0" else "0"
            winner_txt = f"Player 2 wins! ({side})"
        view.curr_turn_label.config(text=winner_txt)
        view.update()

    def _block_btns(self, view: GameFieldView) -> None:
        for i in range(3):
            for j in range(3):
                view.game_btns[i][j].config(state="disabled")

    def _unblock_btns(self, view: GameFieldView) -> None:
        for i in range(3):
            for j in range(3):
                if self._model.game_field[i][j] is None:
                    view.game_btns[i][j].config(state="enabled")

    def update_field(self, view: GameFieldView) -> None:
        for i in range(3):
            for j in range(3):
                tile = self._model.game_field[i][j]
                if tile is None:
                    continue
                view.game_btns[i][j].config(text=f"\n{tile}\n", state="disabled")

    def start(self, root: Tk, data: dict) -> ttk.Frame:
        self.user = data["player 1"]
        opponent = data.get("player 2", None)
        if isinstance(opponent, UserPlayer):
            self.opponent = opponent
        frame = GameView(root)
        self._bind(frame)
        self._turn_callback_rm: Callable = self.user.add_turn_listener(lambda x, y: self.update_game_view(frame, x, y))
        return frame
