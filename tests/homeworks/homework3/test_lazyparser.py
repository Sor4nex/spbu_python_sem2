from src.homeworks.homework3.lazyparser import *
from dataclasses import dataclass
import pytest


@dataclass
class A(metaclass=MetaDataclass):
    param1: int
    param2: str


@dataclass
class B(metaclass=MetaDataclass):
    attr1: A
    attr2: list


@dataclass
class C(metaclass=MetaDataclass):
    attr1: B
    attr2: tuple


def test_metaclass() -> None:
    assert isinstance(A.__dict__["param1"], Descr)
    assert isinstance(A.__dict__["param2"], Descr)
    assert A.__annotations__["param1"] == int
    assert A.__annotations__["param2"] == str


@pytest.mark.parametrize("filename, expected", [
    ("jsons_for_tests/json_dict.json", {"param1": "jaj", "param2": 20}),
    ("jsons_for_tests/json_list.json", {"param1": "jaja", "param2": 21}),
    ("jsons_for_tests/json_list_nested.json", {"param1": [1, 2, 3], "param2": {"param1": [2, 3, 4], "param2": None}})
])
def test_parse_json(filename: str, expected: dict) -> None:
    result = parse_json(filename)
    assert result == expected


def test_parse_json_exception() -> None:
    with pytest.raises(TypeError):
        parse_json("jsons_for_tests/empty_file.json")


def test_parse_class_from_json() -> None:
    result1 = parse_class_from_json(A, "jsons_for_tests/json_A.json")
    assert isinstance(result1.param1, int) and result1.param1 == 100
    assert isinstance(result1.param2, str) and result1.param2 == "esli zakrou bez peresdach vipu pivaaaaa"
    assert isinstance(A.__dict__["param1"], Descr)
    assert isinstance(A.__dict__["param2"], Descr)

    result2 = parse_class_from_json(B, "jsons_for_tests/json_B.json")
    assert isinstance(result2.attr2, list) and result2.attr2 == ["no", "etomu", "vidno", "ne", "bivat", "hnik("]
    assert isinstance(result2.__dict__["attr1"], RuntimeParser)
    assert result2.attr1 == A(100, "esli zakrou bez peresdach vipu pivaaaaa")
    assert isinstance(result2.__dict__["attr1"], A)

    result3 = parse_class_from_json(C, "jsons_for_tests/json_C.json")
    assert result3.attr2 == (1, 2, 3)
    assert isinstance(result3.__dict__["attr1"], RuntimeParser)
    assert isinstance(result3.attr1.__dict__["attr1"], RuntimeParser)
    assert result3.attr1 == B(A(100, "esli zakrou bez peresdach vipu pivaaaaa"), ["no", "etomu", "vidno", "ne", "bivat", "hnik("])
    assert isinstance(result3.attr1.attr1, A)
    assert isinstance(result3.__dict__["attr1"], B)


@pytest.mark.parametrize("dc, json_path", [
    (A, "jsons_for_tests/json_A.json"),
    (B, "jsons_for_tests/json_B.json"),
    (C, "jsons_for_tests/json_C.json"),
    (A, "jsons_for_tests/json_A_strictness.json")
])
def test_dump_class_to_json(dc, json_path) -> None:
    json1 = parse_json(json_path)
    assert json.loads(dump_class_to_json(parse_class_from_json(dc, json_path))) == json1
