from typing import Mapping

import pytest

from src.homeworks.homework1.registry import *


class TestRegistry:
    registry = Registry()
    registry_with_default = Registry(default=dict)

    @registry.register(name="letter A")
    class A:
        pass

    @registry.register(name="буква А")
    class RussianA:
        pass

    @registry.register(name="letter a")
    class LittleA:
        pass

    @registry.register(name="letter B")
    @registry_with_default.register(name="letter B")
    class B:
        pass

    def test_register(self):
        assert list(self.registry.registry) == ["letter A", "буква А", "letter a", "letter B"]

    def test_register_name_already_exist(self):
        with pytest.raises(ValueError):

            @self.registry.register(name="letter A")
            class Zlodey:
                pass

    def test_register_default_not_set(self):
        assert self.registry.default is None

    def test_register_with_default_default(self):
        assert issubclass(self.registry_with_default.default, dict)

    def test_dispatch(self):
        A = self.registry.dispatch("letter A")
        a = self.registry.dispatch("letter a")
        russian_a = self.registry.dispatch("буква А")
        B = self.registry.dispatch("letter B")
        assert (
            issubclass(A, self.A)
            and issubclass(a, self.LittleA)
            and issubclass(russian_a, self.RussianA)
            and issubclass(B, self.B)
        )

    def test_dispatch_not_exist(self):
        with pytest.raises(KeyError):
            a = self.registry.dispatch("letter C")

    def test_dispatch_with_default(self):
        B = self.registry_with_default.dispatch("letter B")
        assert issubclass(B, self.B)

    def test_dispatch_not_exist_with_default(self):
        default = self.registry_with_default.dispatch("do not exist")
        assert issubclass(default, dict)
