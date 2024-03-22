import collections
from typing import Callable, Generic, Mapping, Optional, Type, TypeVar

SuperClass = TypeVar("SuperClass")


USER_OPTIONS = """Choose dictionary you want:
1.Counter
2.Ordered dict
3.Default dict
input: """


class Registry(Generic[SuperClass]):
    def __init__(self, *, default: Optional[Type[SuperClass]] = None) -> None:
        self.registry: dict[str, Type[SuperClass]] = dict()
        self.default: Optional[Type[SuperClass]] = default

    def register(self, *, name: str) -> Callable[[Type[SuperClass]], Type[SuperClass]]:
        """Returns decorator, registering a class by name"""

        def _substitution_func(cls: Type[SuperClass]) -> Type[SuperClass]:
            self.registry[name] = cls
            return cls

        if name in self.registry:
            raise ValueError(f"name {name} is already used in this registry")
        return _substitution_func

    def dispatch(self, name: str) -> Type[SuperClass]:
        """Search for class in registry by name and returns it. If name not found returns default of ValueError"""
        result = self.registry.get(name, self.default)
        if result is None:
            raise KeyError(f"no class, named {name} in this register")
        return result


def register_showcase() -> None:
    registry_for_dicts = Registry[dict](default=dict)
    registry_for_dicts.register(name="counter")(collections.Counter)
    registry_for_dicts.register(name="ordered dict")(collections.OrderedDict)
    registry_for_dicts.register(name="default dict")(collections.defaultdict)

    user_input = input(USER_OPTIONS).lower()
    dispatched_class = registry_for_dicts.dispatch(user_input)
    result = dispatched_class()

    print("dictionary type:", type(result))
    print("content of dictionary:", result)
    print("add pair (1, lol)")
    result[1] = "lol"
    print("ok!")
    print("add pair (2, kek)")
    result[2] = "kek"
    print("ok!")

    print(f"content of dictionary:", result)
    print("delete pair (2, kek)")
    del result[2]
    print(f"content of dictionary", result)


if __name__ == "__main__":
    register_showcase()
