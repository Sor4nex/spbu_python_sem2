import functools
import json
from dataclasses import asdict, dataclass
from typing import Any, TypeVar

import ijson

K = TypeVar("K")


class DescrORM:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def __get__(self, instance: K, owner: type[K]) -> Any:
        needed = instance.__dict__.get(self.name, None)
        if isinstance(needed, functools.partial):
            instance.__dict__[self.name] = needed = needed()
        return needed

    def __set__(self, instance: K, value: Any) -> None:
        instance.__dict__[self.name] = value


class MetaORM(type):
    def __new__(cls, name: str, bases: Any, dct: dict) -> type:
        new_cls = super().__new__(cls, name, bases, dct)
        setattr(new_cls, "from_json", classmethod(MetaORM.from_json))
        setattr(new_cls, "from_dict", classmethod(MetaORM.from_dict))
        setattr(new_cls, "dump_to_json", MetaORM.dump_to_json)
        return new_cls

    def __init__(cls, name: str, bases: Any, dct: dict) -> None:
        for attr in cls.__annotations__:
            setattr(cls, attr, DescrORM(attr))
        super(MetaORM, cls).__init__(name, bases, dct)

    def from_json(cls: type[Any], json_filename: str, strict: bool = False) -> Any:
        def parse_json(file_name: str) -> dict:
            with open(file_name) as file:
                try:
                    for item in ijson.items(file, ""):
                        if isinstance(item, list):
                            return item[0]
                        return item
                    return {}
                except ijson.IncompleteJSONError:
                    raise TypeError("file is empty")

        return cls.from_dict(parse_json(json_filename), strict)

    def from_dict(cls: type[Any], given_dict: dict, strict: bool = False) -> Any:
        if not strict:
            other_fields = {}
            keys_to_del = []
        cls_fields = cls.__annotations__
        for key in given_dict:
            if key in cls_fields:
                arg_type = cls_fields[key]
                if arg_type not in [int, str, float, list, tuple, dict]:
                    given_dict[key] = functools.partial(arg_type.from_dict, given_dict[key], strict)
                else:
                    given_dict[key] = arg_type(given_dict[key])
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

    def dump_to_json(self: Any) -> str:
        dataclass_dict = asdict(self)
        if hasattr(self, "_other_fields"):
            dataclass_dict.update(self._other_fields)
        return json.dumps(dataclass_dict)
