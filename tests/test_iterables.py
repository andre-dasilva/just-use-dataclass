from dataclasses import dataclass
from decimal import Decimal

import pytest

from dict_to_dataclass import dict_to_dataclass


def test_dict_to_dataclass_iterables():
    @dataclass
    class Iterable:
        list: list[str]
        tuple: tuple[int]
        dict: dict[str, float]

    data = {
        "list": ["a", "b", "c"],
        "tuple": (
            1,
            2.3,
            Decimal("232.88"),
        ),
        "dict": {"a": 1, "b": 2},
    }

    iterable = dict_to_dataclass(data, Iterable)

    assert isinstance(iterable.list, list)
    for i in iterable.list:
        assert isinstance(i, str)
    assert iterable.list == ["a", "b", "c"]

    assert isinstance(iterable.tuple, tuple)
    for i in iterable.tuple:
        assert isinstance(i, int)
    assert iterable.tuple == (
        1,
        2,
        232,
    )

    assert isinstance(iterable.dict, dict)
    for key, value in iterable.dict.items():
        assert isinstance(key, str)
        assert isinstance(value, float)
    assert iterable.dict == {"a": 1.0, "b": 2.0}


def test_dict_to_dataclass_conversion_error():
    @dataclass
    class Error:
        a: int
        b: str

    data = {
        "a": "fail",
        "b": 2,
    }

    with pytest.raises(ValueError):
        dict_to_dataclass(data, Error)
