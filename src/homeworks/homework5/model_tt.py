import abc
from time import sleep
from typing import Any, Callable, Optional

from observer_tt import Observable


class Player(metaclass=abc.ABCMeta):
    def __init__(self, model: "TicTacToe", my_turn: bool) -> None:
        self._model = model
        self.my_turn = Observable(my_turn)

    @abc.abstractmethod
    def make_turn(self, coords: tuple) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def callback_turn_change(self, curr_player: "Player") -> None:
        raise NotImplementedError


class UserPlayer(Player):
    def make_turn(self, coords: tuple) -> None:
        print(coords)
        # self._model.make_turn(self)

    def callback_turn_change(self, curr_player: Player) -> None:
        if curr_player is None:
            del self.my_turn.value
        self.my_turn.value = curr_player is self

    def add_turn_listener(self, callback: Callable) -> Callable:
        return self.my_turn.add_callback(callback)

    def puke(self):
        print("{HSSSS")


class BotPlayer(Player):
    def make_turn(self) -> None:
        self._model.make_turn(self)
        print("turn made")

    def callback_turn_change(self, curr_player: "Player") -> None:
        if curr_player is self:
            print("callback recieved")
            sleep(2)
            self.make_turn()


class TicTacToe:
    def __init__(self):
        self.session = Observable()
        self.players: dict[str, Optional[Player]] = {"player1": None, "player2": None}
        self.game_field: Optional[list[list[Optional[bool]]]] = None
        self.current_turn = Observable()

    def start_game(self, mode: str, is_first_turn: bool) -> None:
        def _construct_game_field() -> list[list[None]]:
            return [[None, None, None] * 3]

        player1 = UserPlayer(self, is_first_turn)
        if mode == "bot":
            player2 = BotPlayer(self, not is_first_turn)
        elif mode == "user":
            player2 = player1
        elif mode == "online_outcome":
            pass
        elif mode == "online_income":
            pass
        self.players["player1"], self.players["player2"] = player1, player2
        self.game_field = _construct_game_field()
        self.current_turn.value = self.players["player1"] if is_first_turn else self.players["player2"]
        self.current_turn.add_callback(player1.callback_turn_change)
        self.current_turn.add_callback(player2.callback_turn_change)
        self.session.value = "game"

    def end_game(self) -> None:
        del self.session.value

    def make_turn(self, player: Player, coords: tuple[int, int]) -> None:
        print(f"player {player} made a move")
        if player is not self.current_turn.value:
            return
        i, j = coords
        player_symbol = player is self.players["player1"]
        if self.game_field[i][j] is None:
            self.game_field[i][j] = player_symbol
        if self.check_win():
            return self.update_victory()
        if self.current_turn.value == self.players["player1"]:
            self.current_turn.value = self.players["player2"]
        else:
            self.current_turn.value = self.players["player1"]

    def check_win(self) -> bool:
        horizontal_player1 = any([all(self.game_field[i]) for i in range(3)])
        vertical_player1 = any([all([self.game_field[i][j] for i in range(3)]) for j in range(3)])
        diagonal_player1 = all([self.game_field[i][i] for i in range(3)]) or all([self.game_field[len(self.game_field) - i][i] for i in range(3)])

        horizontal_player2 = any([not any(self.game_field[i]) for i in range(3)])
        vertical_player2 = any([not any([self.game_field[i][j] for i in range(3)]) for j in range(3)])
        diagonal_player2 = not any([self.game_field[i][i] for i in range(3)]) or not any([self.game_field[len(self.game_field) - i][i] for i in range(3)])

        return any([vertical_player1, horizontal_player1, diagonal_player1, vertical_player2, horizontal_player2, diagonal_player2])

    def update_victory(self) -> None:
        del self.current_turn.value
        player1, player2 = self.players["player1"], self.players["player2"]
        self.players["player1"] = self.players["player2"] = None
        del player1, player2

    def add_session_listener(self, callback: Callable) -> Callable:
        return self.session.add_callback(callback)
