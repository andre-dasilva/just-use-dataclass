import typing
from dataclasses import dataclass

import pytest

from dict_to_dataclass import dict_to_dataclass


def test_dict_to_dataclass_nested():
    from dataclasses import dataclass
    from decimal import Decimal

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
