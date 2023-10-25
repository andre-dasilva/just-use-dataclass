from dataclasses import dataclass
from decimal import Decimal

from just_use_dataclass import dict_to_dataclass


@dataclass
class Iterable:
    list: list[str]
    dict: dict[str, float]
    tuple_one: tuple[int]
    tuple_two: tuple[int, str]
    tuple_multiple: tuple[int, ...]


def test_dict_to_dataclass_iterables():
    data = {
        "list": ["a", "b", "c"],
        "tuple_one": (1,),
        "tuple_two": (
            1,
            42,
        ),
        "tuple_multiple": (1, 2.3, Decimal("232.88"), 4.0, 42),
        "dict": {"a": 1, "b": 2},
    }

    iterable = dict_to_dataclass(data, Iterable)

    assert isinstance(iterable.list, list)
    for i in iterable.list:
        assert isinstance(i, str)
    assert iterable.list == ["a", "b", "c"]

    assert isinstance(iterable.tuple_one, tuple)
    assert isinstance(iterable.tuple_one[0], int)
    assert iterable.tuple_one == (1,)

    assert isinstance(iterable.tuple_two, tuple)
    assert isinstance(iterable.tuple_two[0], int)
    assert isinstance(iterable.tuple_two[1], str)
    assert iterable.tuple_two == (1, "42")

    assert isinstance(iterable.tuple_multiple, tuple)
    for t in iterable.tuple_multiple:
        assert isinstance(t, int)
    assert iterable.tuple_multiple == (1, 2, 232, 4, 42)

    assert isinstance(iterable.dict, dict)
    for key, value in iterable.dict.items():
        assert isinstance(key, str)
        assert isinstance(value, float)
    assert iterable.dict == {"a": 1.0, "b": 2.0}
