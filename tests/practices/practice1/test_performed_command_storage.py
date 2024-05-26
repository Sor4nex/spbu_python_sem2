from io import StringIO

import pytest

from src.practices.practice1.performed_command_storage import *


class TestPerformedCommandStorage:
    init_list = []
    storage = PerformedCommandStorage(init_list)

    action1 = acts.ActionInsertStart(55)
    action2 = acts.ActionInsertEnd(33)
    action3 = acts.ActionInsertEnd(22)
    action4 = acts.ActionReverse()

    def test_command_storage_apply(self) -> None:
        assert self.storage.is_empty()

        self.storage.apply(self.action1)

        assert self.storage.commands_list == [self.action1]
        assert self.storage.object_list == [55]
        assert not self.storage.is_empty()

        self.storage.apply(self.action2)
        self.storage.apply(self.action3)
        self.storage.apply(self.action4)

        assert self.storage.commands_list == [self.action1, self.action2, self.action3, self.action4]
        assert self.storage.object_list == [22, 33, 55]
        assert not self.storage.is_empty()

    def test_command_storage_undo(self) -> None:
        self.storage.undo()

        assert self.storage.commands_list == [self.action1, self.action2, self.action3]
        assert self.storage.object_list == [55, 33, 22]

        self.storage.undo()
        self.storage.undo()

        assert self.storage.commands_list == [self.action1]
        assert self.storage.object_list == [55]

        self.storage.undo()

        assert self.storage.commands_list == []
        assert self.storage.object_list == []
        assert self.storage.is_empty()

        with pytest.raises(ValueError):
            self.storage.undo()


class TestPerformedCommandStorageMain:
    @pytest.mark.parametrize(
        "user_input, expected_output",
        [
            (["exit"], [""]),
            (["shiiiish", "exit"], [ERROR_ACTION_NOT_FOUND.format("shiiiish"), INFO_LIST_CONDITION.format([], 0), ""]),
            (
                ["insert_start 1", "undo", "exit"],
                [INFO_LIST_CONDITION.format([1], 1), INFO_LIST_CONDITION.format([], 0), ""],
            ),
            (
                ["undo", "exit"],
                ["\nerror: command storage has nothing to undo \n", INFO_LIST_CONDITION.format([], 0), ""],
            ),
            (
                ["insert_start 2", "add 0 2", "undo", "undo", "exit"],
                [
                    INFO_LIST_CONDITION.format([2], 1),
                    INFO_LIST_CONDITION.format([4], 1),
                    INFO_LIST_CONDITION.format([2], 1),
                    INFO_LIST_CONDITION.format([], 0),
                    "",
                ],
            ),
            (
                ["insert_end 3", "undo", "undo", "exit"],
                [
                    INFO_LIST_CONDITION.format([3], 1),
                    INFO_LIST_CONDITION.format([], 0),
                    "\nerror: command storage has nothing to undo \n",
                    INFO_LIST_CONDITION.format([], 0),
                    "",
                ],
            ),
            (["insert ivanov aleksei", "exit"], [ERROR_WRONG_ARGS_TYPE, INFO_LIST_CONDITION.format([], 0), ""]),
            (["add 1234 4", "exit"], [ERROR_WRONG_INDEX, INFO_LIST_CONDITION.format([], 0), ""]),
        ],
    )
    def test_main(self, monkeypatch, user_input, expected_output) -> None:
        monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
        fake_output = StringIO()
        monkeypatch.setattr("sys.stdout", fake_output)
        main()
        output = fake_output.getvalue()
        expected_output.insert(0, INFO_LIST_CONDITION.format([], 0))
        assert output == "\n".join(expected_output)
