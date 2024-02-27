from typing import Callable, Generic, Optional, TypeVar

Interface = TypeVar("Interface")


class Registry(Generic[Interface]):
    def __init__(self, *, default: Optional[Interface] = None) -> None:
        self.registry: dict[str, Interface] = dict()
        self.default: Optional[Interface] = default

    def register(self, *, name: str) -> Callable[[Interface], Interface]:
        """Returns decorator, registering a class by name"""

        def _substitution_func(cls: Interface) -> Interface:
            self.registry[name] = cls
            return cls

        if name in self.registry:
            raise ValueError(f"name {name} is already used in this registry")
        return _substitution_func

    def dispatch(self, name: str) -> Interface:
        """Search for class in registry by name and returns it. If name not found returns default of ValueError"""
        if name not in self.registry.keys():
            if self.default is not None:
                return self.default
            raise ValueError(f"no class, named {name} in this register")
        return self.registry[name]
