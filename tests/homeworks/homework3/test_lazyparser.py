from src.homeworks.homework3.lazyparser import *
from dataclasses import dataclass
import pytest


class TestLazyParser:
    @dataclass
    class A(metaclass=MetaDataclass):
        param1: int
        param2: str

    @dataclass
    class B(metaclass=MetaDataclass):
        attr1: self.A
        attr2: list

    def check_parser_resulting_object(self, cls, obj) -> bool:
        pass

    def test_metaclass(self) -> None:
        assert isinstance(self.A.__dict__["param1"], Descr)
        assert isinstance(self.A.__dict__["param2"], Descr)
        assert self.A.__annotations__["param1"] == int
        assert self.A.__annotations__["param2"] == str

    @pytest.mark.parametrize("filename, expected", [
        ("jsons_for_tests/json_dict.json", {"param1": "jaj", "param2": 20}),
        ("jsons_for_tests/json_list.json", {"param1": "jaja", "param2": 21})
    ])
    def test_parse_json(self, filename: str, expected: dict) -> None:
        result = parse_json(filename)
        assert result == expected

    def test_parse_json_exception(self) -> None:
        with pytest.raises(TypeError):
            parse_json("jsons_for_tests/empty_file.json")

    def test_parse_class_from_json(self) -> None:
        result = parse_class_from_json(self.A, "jsons_for_tests/json_list.json")


