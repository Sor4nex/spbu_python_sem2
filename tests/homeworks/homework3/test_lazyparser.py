import functools
from dataclasses import dataclass

import pytest

from src.homeworks.homework3.lazyparser import *


@dataclass
class A(JsonORM):
    param1: int
    param2: str


@dataclass
class B(JsonORM):
    attr1: A
    attr2: list


@dataclass
class C(JsonORM):
    attr1: B
    attr2: tuple


def parse_json(file_name: str) -> dict:
    with open(file_name) as file:
        return json.load(file)[0]


def test_metaclass() -> None:
    A.from_json_dict({})
    assert isinstance(A.__dict__["param1"], DescrORM)
    assert isinstance(A.__dict__["param2"], DescrORM)
    assert A.__annotations__["param1"] == int
    assert A.__annotations__["param2"] == str


def test_parse_class_from_json() -> None:
    json1 = parse_json("tests/homeworks/homework3/jsons_for_tests/json_A.json")
    result1 = A.from_json_dict(json1)
    assert isinstance(result1.param1, int) and result1.param1 == 100
    assert isinstance(result1.param2, str) and result1.param2 == "esli zakrou bez peresdach vipu pivaaaaa"
    assert isinstance(A.__dict__["param1"], DescrORM)
    assert isinstance(A.__dict__["param2"], DescrORM)

    json2 = parse_json("tests/homeworks/homework3/jsons_for_tests/json_B.json")
    result2 = B.from_json_dict(json2)
    assert isinstance(result2.attr2, list) and result2.attr2 == ["no", "etomu", "vidno", "ne", "bivat", "hnik("]
    assert result2.__dict__["attr1"] is None
    assert result2.attr1 == A(100, "esli zakrou bez peresdach vipu pivaaaaa")
    assert isinstance(result2.__dict__["attr1"], A)

    json3 = parse_json("tests/homeworks/homework3/jsons_for_tests/json_C.json")
    result3 = C.from_json_dict(json3)
    assert result3.attr2 == (1, 2, 3)
    assert result3.__dict__["attr1"] is None
    assert result3.attr1.__dict__["attr1"] is None
    assert result3.attr1 == B(
        A(100, "esli zakrou bez peresdach vipu pivaaaaa"), ["no", "etomu", "vidno", "ne", "bivat", "hnik("]
    )
    assert isinstance(result3.attr1.attr1, A)
    assert isinstance(result3.__dict__["attr1"], B)


@pytest.mark.parametrize(
    "dc, json_path",
    [
        (A, "tests/homeworks/homework3/jsons_for_tests/json_A.json"),
        (B, "tests/homeworks/homework3/jsons_for_tests/json_B.json"),
        (C, "tests/homeworks/homework3/jsons_for_tests/json_C.json"),
    ],
)
def test_dump_to_json(dc, json_path) -> None:
    json1 = parse_json(json_path)
    obj = dc.from_json_dict(json1)
    assert json.loads(obj.dump_to_json()) == parse_json(json_path)
