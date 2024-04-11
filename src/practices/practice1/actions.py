import abc
from typing import Optional

import src.homeworks.homework1.registry as registry

ACTIONS_REGISTRY = registry.Registry["Action"]()


class Action(metaclass=abc.ABCMeta):
    def __init__(self, *args: Optional[int]) -> None:
        self.args: list = list(args)

    @abc.abstractmethod
    def apply(self, given_list: list) -> None:
        pass

    @abc.abstractmethod
    def undo(self, given_list: list) -> None:
        pass


@ACTIONS_REGISTRY.register(name="insert")
class ActionInsert(Action):
    def apply(self, given_list: list) -> None:
        given_list.insert(self.args[0], self.args[1])

    def undo(self, given_list: list) -> None:
        given_list.pop(self.args[0])


@ACTIONS_REGISTRY.register(name="insert_start")
class ActionInsertStart(Action):
    def apply(self, given_list: list) -> None:
        given_list.insert(0, self.args[0])

    def undo(self, given_list: list) -> None:
        given_list.pop(0)


@ACTIONS_REGISTRY.register(name="insert_end")
class ActionInsertEnd(Action):
    def apply(self, given_list: list) -> None:
        given_list.append(self.args[0])

    def undo(self, given_list: list) -> None:
        given_list.pop()


@ACTIONS_REGISTRY.register(name="change_positions")
class ActionChangePositions(Action):
    def apply(self, given_list: list) -> None:
        given_list[self.args[0]], given_list[self.args[1]] = given_list[self.args[1]], given_list[self.args[0]]

    def undo(self, given_list: list) -> None:
        self.apply(given_list)


@ACTIONS_REGISTRY.register(name="add")
class ActionAddition(Action):
    def apply(self, given_list: list) -> None:
        given_list[self.args[0]] += self.args[1]

    def undo(self, given_list: list) -> None:
        given_list[self.args[0]] -= self.args[1]


@ACTIONS_REGISTRY.register(name="subtract")
class ActionSubtraction(Action):
    def apply(self, given_list: list) -> None:
        given_list[self.args[0]] -= self.args[1]

    def undo(self, given_list: list) -> None:
        given_list[self.args[0]] += self.args[1]


@ACTIONS_REGISTRY.register(name="reverse")
class ActionReverse(Action):
    def apply(self, given_list: list) -> None:
        given_list.reverse()

    def undo(self, given_list: list) -> None:
        self.apply(given_list)


@ACTIONS_REGISTRY.register(name="add_to_all")
class ActionAdditionAll(Action):
    def apply(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] += self.args[0]

    def undo(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] -= self.args[0]


@ACTIONS_REGISTRY.register(name="subtract_from_all")
class ActionSubtractionAll(Action):
    def apply(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] -= self.args[0]

    def undo(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] += self.args[0]


@ACTIONS_REGISTRY.register(name="remove")
class ActionRemove(Action):
    def apply(self, given_list: list) -> None:
        removed_element = given_list.pop(self.args[0])
        self.args.append(removed_element)

    def undo(self, given_list: list) -> None:
        if len(self.args) < 2:
            raise ValueError("cannot undo, apply was not used")
        given_list.insert(self.args[0], self.args[1])
