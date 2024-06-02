import functools
import json
from dataclasses import asdict, dataclass
from typing import Any, Type, TypeVar, get_args

K = TypeVar("K")


def get_from_json_dict(instance: K, name: str) -> Any:
    if not hasattr(instance, "__json_data__"):
        raise KeyError("instance was not initialized with json")
    json_dict = getattr(instance, "__json_data__")
    json_value = json_dict.get(name, None)
    if json_value is None:
        raise KeyError(f"json does not have attribute {name}")
    value_type = instance.__annotations__[name]
    if value_type in [int, float, str, list, tuple, dict]:
        return value_type(json_value)
    return value_type.from_json_dict(json_value)


class DescrORM:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def __get__(self, instance: K, owner: type[K]) -> Any:
        if instance is None:
            return self
        needed = instance.__dict__.get(self.name, None)
        if needed is None:
            new_value = get_from_json_dict(instance, self.name)
            instance.__dict__[self.name] = needed = new_value
        return needed

    def __set__(self, instance: K, value: Any) -> None:
        instance.__dict__[self.name] = value


@dataclass
class JsonORM:
    @classmethod
    def from_json_dict(cls: Type[K], json_dict: dict, strict: bool = False) -> K:
        if strict and (set(json_dict.keys()) != set(cls.__annotations__.keys())):
            raise ValueError("invalid json: some json fields differ from class fields")
        for field in cls.__annotations__:
            setattr(cls, field, DescrORM(field))
        instance = cls(*[None for _ in range(len(cls.__annotations__))])
        setattr(instance, "__json_data__", json_dict)
        return instance

    def dump_to_json(self) -> str:
        return json.dumps(asdict(self))
