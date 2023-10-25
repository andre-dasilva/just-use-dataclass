import math
import typing
from dataclasses import dataclass
from decimal import Decimal

from just_use_dataclass import dict_to_dataclass


@dataclass
class Simple:
    a: str
    b: int
    c: float
    d: bool
    e: typing.Optional[str]
    f: typing.Optional[str]
    g: typing.Optional[int]
    h: typing.Optional[Decimal]


def test_dict_to_dataclass_simple():
    data = {
        "a": 1,
        "b": "1",
        "c": "2.0",
        "d": True,
        "e": None,
        "f": 42,
        "g": 2,
        "h": 39.1012,
    }

    simple = dict_to_dataclass(data, Simple)

    assert isinstance(simple.a, str)
    assert simple.a == "1"

    assert isinstance(simple.b, int)
    assert simple.b == 1

    assert isinstance(simple.c, float)
    assert math.isclose(simple.c, 2.0, abs_tol=0.00001)

    assert isinstance(simple.d, bool)
    assert simple.d is True

    assert simple.e is None

    assert isinstance(simple.f, str)
    assert simple.f == "42"

    assert isinstance(simple.g, int)
    assert simple.g == 2

    assert isinstance(simple.h, Decimal)
    assert simple.h == Decimal("39.1012")
