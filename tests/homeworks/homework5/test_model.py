import pytest

from src.homeworks.homework5.model_tt import *


class TestModel:
    model1 = TicTacToe()

    def test_model_init(self) -> None:
        assert isinstance(self.model1.session, Observable)
        assert self.model1.session.value is None
        assert self.model1.gamemode is None
        assert self.model1.players == {"player1": None, "player2": None}
        assert self.model1.game_field == [[None, None, None] for _ in range(3)]
        assert isinstance(self.model1.current_turn, Observable)

    @pytest.mark.parametrize(
        "mode, is_first_turn, ip, port, expected_opp",
        [
            ("Easy bot", True, "", BotPlayerEasy),
            ("Easy bot", False, "", BotPlayerEasy),
            ("Hard bot", True, "", BotPlayerHard),
            ("Hard bot", False, "", BotPlayerHard),
            ("One computer", True, "", UserPlayer),
            ("One computer", False, "", UserPlayer)
        ],
    )
    def test_model_start_game(self, mode, is_first_turn, ip, port, expected_opp) -> None:
        self.model1.start_game(mode, is_first_turn, ip, port)

        assert isinstance(self.model1.players["player1"], UserPlayer)
        assert self.model1.players["player1"].side == "X" if is_first_turn else "0"
        assert isinstance(self.model1.players["player2"], expected_opp)
        assert self.model1.players["player2"].side == "0" if is_first_turn else "X"

    def test_end_game(self) -> None:
        self.model1.start_game("One computer", True, "", "")
        self.model1.end_game()

        assert self.model1.session.value is None

    def test_make_turn(self) -> None:
        self.model1.start_game("One computer", True, "", "")
        assert self.model1.game_field == [[None, None, None] for _ in range(3)]

        self.model1.make_turn(self.model1.players["player1"], (0, 0))
        assert self.model1.game_field == [["X", None, None]] + [[None, None, None] for _ in range(2)]

        self.model1.make_turn(self.model1.players["player2"], (0, 1))
        assert self.model1.game_field == [["X", "0", None]] + [[None, None, None] for _ in range(2)]

        self.model1.make_turn(self.model1.players["player1"], (1, 2))
        assert self.model1.game_field == [["X", "0", None], [None, None, "X"], [None, None, None]]

    @pytest.mark.parametrize(
        "field, expected",
        [
            ([[None, None, None], [None, None, None], [None, None, None]], False),
            ([["X", None, None], ["X", None, None], ["X", None, None]], True),
            ([[None, "X", None], [None, "X", None], [None, "X", None]], True),
            ([[None, None, "X"], [None, None, "X"], [None, None, "X"]], True),
            ([["X", None, None], [None, "X", None], [None, None, "X"]], True),
            ([[None, None, "X"], [None, "X", None], ["X", None, None]], True),
            ([[None, None, "X"], [None, "X", None], ["0", None, None]], False),
            ([[None, None, "X"], [None, "X", None], [None, None, None]], False),
            ([["0", None, None], ["0", None, None], ["0", None, None]], True),
            ([[None, "0", None], [None, "0", None], [None, "0", None]], True),
            ([[None, None, "0"], [None, None, "0"], [None, None, "0"]], True),
            ([["0", None, None], [None, "0", None], [None, None, "0"]], True),
            ([[None, None, "0"], [None, "0", None], ["0", None, None]], True),
            ([["0", None, None], ["0", None, None], [None, None, None]], False),
            ([[None, "0", None], [None, "0", None], [None, "X", None]], False),
            ([["0", "X", None], ["0", "X", None], ["0", None, None]], True),
        ],
    )
    def test_check_win(self, field, expected) -> None:
        assert self.model1.check_win(field) == expected

    def test_update_draw(self) -> None:
        self.model1.start_game("One computer", True, "", "")
        self.model1.update_draw()

        assert self.model1.current_turn.value is None
        assert self.model1.gamemode is None
        assert self.model1.players == {}

    def test_update_victory(self) -> None:
        self.model1.start_game("One computer", True, "", "")
        self.model1.update_victory()

        assert self.model1.current_turn.value is None
        assert self.model1.gamemode is None
        assert self.model1.players == {}
