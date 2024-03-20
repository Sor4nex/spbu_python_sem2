from typing import Callable, Generic, Optional, TypeVar
from functools import wraps


I = TypeVar("I")


class Registry(Generic[I]):
    def __init__(self, *, default: Optional[I] = None) -> None:
        self.registry: dict[str, I] = dict()
        self.default: Optional[I] = default

    def register(self, *, name: str) -> Callable[[I], I]:
        """Returns decorator, registering a class by name"""
        def _substitution_func(cls: I) -> I:
            self.registry[name] = cls
            return cls

        if name in self.registry:
            raise ValueError(f"name {name} is already used in this registry")
        return _substitution_func

    def dispatch(self, name: str) -> Optional[I]:
        """Search for class in registry by name and returns it. If name not found returns default of ValueError"""
        result = self.registry.get(name, self.default)
        if result is None:
            raise KeyError(f"no class, named {name} in this register")
        return result
