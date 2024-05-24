from types import GenericAlias
from typing import TypeVar, Any
import ijson


K = TypeVar("K")


class Descr:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def __get__(self, instance: K, owner: type[K]) -> Any:
        needed = instance.__dict__[self.name]
        if isinstance(needed, RuntimeParser):
            instance.__dict__[self.name] = needed.parse()
        return instance.__dict__[self.name]

    def __set__(self, instance: K, value: Any) -> None:
        instance.__dict__[self.name] = value


class RuntimeParser:
    def __init__(self, cls: type[K], given_dict: dict, strict: bool) -> None:
        self.cls_to_parse: type[K] = cls
        self.given_dict: dict = given_dict
        self.is_strict: bool = strict

    def parse(self) -> Any:
        return from_dict(self.cls_to_parse, self.given_dict, self.is_strict)


class MetaDataclass(type):
    def __init__(cls, name: str, bases: Any, dct: dict) -> None:
        for attr in cls.__annotations__:
            setattr(cls, attr, Descr(attr))
        super(MetaDataclass, cls).__init__(name, bases, dct)


def parse_json(file_name: str) -> dict:
    with open(file_name) as file:
        try:
            for item in ijson.items(file, ""):
                if isinstance(item, list):
                    return item[0]
                return item
        except ijson.IncompleteJSONError:
            raise TypeError("file is empty")


def parse_class_from_json(cls: type[K], json_filename: str, strict: bool = False) -> K:
    return from_dict(cls, parse_json(json_filename), strict)


def from_dict(cls: type[K], given_dict: dict, strict: bool) -> K:
    if not strict:
        other_fields = dict()
        keys_to_del = []
    cls_fields = cls.__annotations__
    for key in given_dict:
        if key in cls_fields:
            arg_type = cls_fields[key]
            if isinstance(arg_type, GenericAlias):
                arg_type = arg_type.__origin__
            if arg_type not in [int, str, float, list, tuple, dict]:
                given_dict[key] = RuntimeParser(arg_type, given_dict[key], strict)
            continue
        if not strict:
            keys_to_del.append(key)
            other_fields[key] = given_dict[key]
            continue
        raise KeyError("redundant fields were found")
    if not strict:
        for key in keys_to_del:
            del given_dict[key]
    try:
        result = cls(**given_dict)
        if not strict:
            setattr(result, "_other_fields", other_fields)
        return result
    except TypeError:
        raise KeyError("some dataclass fields left empty")
