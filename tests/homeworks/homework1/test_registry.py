from typing import Mapping

import pytest

from src.homeworks.homework1.registry import *

registry = Registry[Mapping]()
registry_with_default = Registry[Mapping](default=dict)


@registry.register(name="lol")
class MapLol(Mapping):
    def __init__(self) -> None:
        pass

    def __iter__(self) -> None:
        pass

    def __getitem__(self, item) -> None:
        pass

    def __len__(self) -> None:
        pass


@registry.register(name="kek")
class MapKek(Mapping):
    def __init__(self) -> None:
        pass

    def __iter__(self) -> None:
        pass

    def __getitem__(self, item) -> None:
        pass

    def __len__(self) -> None:
        pass


def test_register() -> None:
    assert (
        isinstance(registry.registry["lol"](), MapLol)
        and isinstance(registry.registry["kek"](), MapKek)
        and isinstance(registry_with_default.default(), dict)
    )


def test_dispatch() -> None:
    assert (
        isinstance(registry.dispatch("lol")(), MapLol)
        and isinstance(registry.dispatch("kek")(), MapKek)
        and isinstance(registry_with_default.dispatch("чтоточегонет")(), dict)
    )


def test_register_exception_case() -> None:
    with pytest.raises(ValueError):

        @registry.register(name="lol")
        class YaUpal(Mapping):
            pass


def test_dispatch_exception_case() -> None:
    with pytest.raises(ValueError):
        registry.dispatch(name="этогоНетВЭтомРегистре")
