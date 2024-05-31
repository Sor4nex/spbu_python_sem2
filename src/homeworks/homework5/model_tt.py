import abc
import copy
import random
from typing import Any, Callable, Optional

from src.homeworks.homework5.observer_tt import Observable


class Player(metaclass=abc.ABCMeta):
    def __init__(self, model: "TicTacToe", my_turn: bool) -> None:
        self._model = model
        self.side = "X" if my_turn else "0"
        self.my_turn = Observable(my_turn)

    @abc.abstractmethod
    def make_turn(self, coords: tuple[int, int]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def callback_turn_change(self, curr_player: "Player", additional: dict) -> None:
        raise NotImplementedError


class UserPlayer(Player):
    def make_turn(self, coords: tuple[int, int]) -> None:
        self._model.make_turn(self, coords)

    def callback_turn_change(self, curr_player: Player, additional: dict) -> None:
        if curr_player is None:
            self.my_turn.additional_info = additional
            self.my_turn.value = None
            return
        self.my_turn.value = curr_player is self

    def add_turn_listener(self, callback: Callable) -> Callable:
        return self.my_turn.add_callback(callback)


class BotPlayer(Player):
    def make_turn(self, coords: tuple[int, int]) -> None:
        self._model.make_turn(self, coords)

    def callback_turn_change(self, curr_player: "Player", additional: dict) -> None:
        if curr_player is self:
            self.play_game()

    def play_game(self) -> None:
        raise NotImplementedError


class BotPlayerEasy(BotPlayer):
    def play_game(self) -> None:
        available_places = [(i, j) for i in range(3) for j in range(3) if self._model.game_field[i][j] is None]
        move = random.choice(available_places)
        self.make_turn(move)


class BotPlayerHard(BotPlayer):
    def play_game(self) -> None:
        opponent_side = "X" if self.side == "0" else "0"
        local_field = copy.deepcopy(self._model.game_field)
        available_places = [(i, j) for i in range(3) for j in range(3) if local_field[i][j] is None]

        for coords in available_places:
            i, j = coords
            local_field[i][j] = self.side
            if self._model.check_win(local_field):
                return self.make_turn((i, j))
            local_field[i][j] = None

        for coords in available_places:
            i, j = coords
            local_field[i][j] = opponent_side
            if self._model.check_win(local_field):
                return self.make_turn((i, j))
            local_field[i][j] = None

        move = random.choice(available_places)
        self.make_turn(move)


class TicTacToe:
    def __init__(self) -> None:
        self.session: Observable = Observable()
        self.gamemode: Optional[str] = None
        self.players: dict[str, Optional[Player]] = {"player1": None, "player2": None}
        self.game_field: list[list[Optional[str]]] = [[None, None, None] for _ in range(3)]
        self.current_turn: Observable = Observable()

    def start_game(self, mode: str, is_first_turn: bool, ip: str) -> None:
        def _construct_game_field() -> list[list[Optional[str]]]:
            return [[None, None, None] for _ in range(3)]

        player1 = UserPlayer(self, is_first_turn)
        player2: Optional[Player] = None
        if mode == "Easy bot":
            self.gamemode = "bot"
            player2 = BotPlayerEasy(self, not is_first_turn)
        elif mode == "Hard bot":
            self.gamemode = "bot"
            player2 = BotPlayerHard(self, not is_first_turn)
        elif mode == "One computer":
            self.gamemode = "user"
            player1.side = "X"
            player2 = player1
        elif mode == "Connect to game":
            pass
        elif mode == "Create the game":
            pass
        else:
            return
        self.players["player1"], self.players["player2"] = player1, player2
        self.game_field = _construct_game_field()
        self.session.value = "game"
        if player1 is not None and player2 is not None:
            self.current_turn.add_callback(player1.callback_turn_change)
            self.current_turn.add_callback(player2.callback_turn_change)
        self.current_turn.value = self.players["player1"] if is_first_turn else self.players["player2"]

    def end_game(self) -> None:
        del self.session.value

    def make_turn(self, player: Player, coords: tuple[int, int]) -> None:
        if player is not self.current_turn.value:
            return
        i, j = coords
        if self.game_field[i][j] is None:
            self.game_field[i][j] = player.side
        if self.check_win(self.game_field):
            return self.update_victory()
        if all(all(self.game_field[i][j] is not None for i in range(3)) for j in range(3)):
            return self.update_draw()
        if self.gamemode == "user":
            player.side = "X" if player.side == "0" else "0"
        if self.current_turn.value == self.players["player1"]:
            self.current_turn.value = self.players["player2"]
        else:
            self.current_turn.value = self.players["player1"]

    def check_win(self, game_field: list[list[Optional[str]]]) -> bool:
        is_x = lambda x: x == "X"
        is_y = lambda y: y == "0"
        horizontal_player1 = any([all(is_x(game_field[i][j]) for j in range(3)) for i in range(3)])
        vertical_player1 = any([all([is_x(game_field[i][j]) for i in range(3)]) for j in range(3)])
        diagonal_player1 = all([is_x(game_field[i][i]) for i in range(3)]) or all(
            [is_x(game_field[len(game_field) - i - 1][i]) for i in range(3)]
        )

        horizontal_player2 = any([all(is_y(game_field[i][j]) for j in range(3)) for i in range(3)])
        vertical_player2 = any([all([is_y(game_field[i][j]) for i in range(3)]) for j in range(3)])
        diagonal_player2 = all([is_y(game_field[i][i]) for i in range(3)]) or all(
            [is_y(game_field[len(game_field) - i - 1][i]) for i in range(3)]
        )

        return any(
            [
                vertical_player1,
                horizontal_player1,
                diagonal_player1,
                vertical_player2,
                horizontal_player2,
                diagonal_player2,
            ]
        )

    def update_draw(self) -> None:
        self.current_turn.additional_info["winner"] = "Draw"
        del self.current_turn.value
        self.gamemode = None
        del self.players["player1"], self.players["player2"]

    def update_victory(self) -> None:
        if self.current_turn.value is not None:
            self.current_turn.additional_info["winner"] = (
                f"Player 1 wins! ({self.current_turn.value.side})"
                if self.current_turn.value == self.players["player1"]
                else f"Player2 wins! ({self.current_turn.value.side})"
            )
        del self.current_turn.value
        self.gamemode = None
        del self.players["player1"], self.players["player2"]

    def add_session_listener(self, callback: Callable) -> Callable:
        return self.session.add_callback(callback)
