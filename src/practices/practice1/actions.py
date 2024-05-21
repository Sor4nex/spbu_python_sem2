import abc
from typing import Any, Optional

import src.homeworks.homework1.registry as registry

ACTIONS_REGISTRY = registry.Registry["Action"]()


class Action(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, given_list: list) -> None:
        pass

    @abc.abstractmethod
    def undo(self, given_list: list) -> None:
        pass


@ACTIONS_REGISTRY.register(name="insert")
class ActionInsert(Action):
    def __init__(self, index: int, value: Any) -> None:
        self.index = index
        self.value = value

    def apply(self, given_list: list) -> None:
        given_list.insert(self.index, self.value)

    def undo(self, given_list: list) -> None:
        given_list.pop(self.index)


@ACTIONS_REGISTRY.register(name="insert_start")
class ActionInsertStart(Action):
    def __init__(self, value: Any) -> None:
        self.value = value

    def apply(self, given_list: list) -> None:
        given_list.insert(0, self.value)

    def undo(self, given_list: list) -> None:
        given_list.pop(0)


@ACTIONS_REGISTRY.register(name="insert_end")
class ActionInsertEnd(Action):
    def __init__(self, value: Any) -> None:
        self.value = value

    def apply(self, given_list: list) -> None:
        given_list.append(self.value)

    def undo(self, given_list: list) -> None:
        given_list.pop()


@ACTIONS_REGISTRY.register(name="change_positions")
class ActionChangePositions(Action):
    def __init__(self, pos1: int, pos2: int):
        self.pos1 = pos1
        self.pos2 = pos2

    def apply(self, given_list: list) -> None:
        given_list[self.pos1], given_list[self.pos2] = given_list[self.pos2], given_list[self.pos1]

    def undo(self, given_list: list) -> None:
        self.apply(given_list)


@ACTIONS_REGISTRY.register(name="add")
class ActionAddition(Action):
    def __init__(self, index: int, value: Any) -> None:
        self.index = index
        self.value = value

    def apply(self, given_list: list) -> None:
        given_list[self.index] += self.value

    def undo(self, given_list: list) -> None:
        given_list[self.index] -= self.value


@ACTIONS_REGISTRY.register(name="subtract")
class ActionSubtraction(Action):
    def __init__(self, index: int, value: Any) -> None:
        self.index = index
        self.value = value

    def apply(self, given_list: list) -> None:
        given_list[self.index] -= self.value

    def undo(self, given_list: list) -> None:
        given_list[self.index] += self.value


@ACTIONS_REGISTRY.register(name="reverse")
class ActionReverse(Action):
    def apply(self, given_list: list) -> None:
        given_list.reverse()

    def undo(self, given_list: list) -> None:
        self.apply(given_list)


@ACTIONS_REGISTRY.register(name="add_to_all")
class ActionAdditionAll(Action):
    def __init__(self, value: Any) -> None:
        self.value = value

    def apply(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] += self.value

    def undo(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] -= self.value


@ACTIONS_REGISTRY.register(name="subtract_from_all")
class ActionSubtractionAll(Action):
    def __init__(self, value: Any) -> None:
        self.value = value

    def apply(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] -= self.value

    def undo(self, given_list: list) -> None:
        for i in range(len(given_list)):
            given_list[i] += self.value


@ACTIONS_REGISTRY.register(name="remove")
class ActionRemove(Action):
    def __init__(self, index: int):
        self.index = index
        self.removed_element: Optional[Any] = None

    def apply(self, given_list: list) -> None:
        removed_element = given_list.pop(self.index)
        self.removed_element = removed_element

    def undo(self, given_list: list) -> None:
        if self.removed_element is None:
            raise ValueError("cannot undo, apply was not used")
        given_list.insert(self.index, self.removed_element)
