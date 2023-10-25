from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from dict_to_dataclass import dict_to_dataclass


@dataclass
class C:
    value: str


@dataclass
class B:
    value: int
    c: C


@dataclass
class A:
    value_1: Decimal
    value_2: Decimal
    b: B


def test_dict_to_dataclass_nested():
    data = {
        "value_1": "23.23",
        "value_2": 49.0001,
        "b": {
            "value": 1,
            "c": {"value": "test"},
        },
    }

    nested = dict_to_dataclass(data, A)

    assert isinstance(nested.value_1, Decimal)
    assert nested.value_1 == Decimal("23.23")

    assert isinstance(nested.value_2, Decimal)
    assert nested.value_2 == Decimal("49.0001")

    assert isinstance(nested.b, B)

    assert isinstance(nested.b.value, int)
    assert nested.b.value == 1

    assert isinstance(nested.b.c, C)

    assert isinstance(nested.b.c.value, str)
    assert nested.b.c.value == "test"


@dataclass
class C2:
    value: list[Optional[str]]


@dataclass
class B2:
    value: Optional[list[Decimal]]
    c: C2


def test_dict_to_dataclass_nested_types():
    data = {"value": [1, 2, 3], "c": {"value": [None, 1, "test", "world", 2.0, True]}}

    nested = dict_to_dataclass(data, B2)

    assert isinstance(nested, B2)

    assert nested.value is not None
    for v in nested.value:
        assert isinstance(v, Decimal)
    assert nested.value == [Decimal("1"), Decimal("2"), Decimal("3")]

    assert isinstance(nested.c.value, list)
    for v in nested.c.value:
        assert isinstance(v, str) or v is None
    assert nested.c.value == [None, "1", "test", "world", "2.0", "True"]


@dataclass
class Crazy:
    value: dict[str, dict[int, list[Optional[str]]]]


def test_dict_to_dataclass_nested_crazy():
    data = {"value": {"test": {1: ["hey", None, 42]}}}

    crazy = dict_to_dataclass(data, Crazy)

    assert isinstance(crazy.value, dict)
    assert isinstance(crazy.value["test"], dict)
    assert isinstance(crazy.value["test"][1], list)
    assert crazy.value["test"][1] == ["hey", None, "42"]
