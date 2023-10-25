import typing
from dataclasses import dataclass

import pytest

from just_use_dataclass import dict_to_dataclass


@dataclass
class Error:
    a: int
    b: str
    c: typing.Union[str, int]


def test_dict_to_dataclass_conversion_error():
    data = {
        "a": "fail",
        "b": 2,
    }

    with pytest.raises(ValueError):
        dict_to_dataclass(data, Error)


def test_dict_to_dataclass_missing_field_error():
    data = {
        "a": 1,
        "not_in_error": 2,
    }

    with pytest.raises(ValueError):
        dict_to_dataclass(data, Error)


def test_dict_to_dataclass_union():
    data = {"a": 2, "b": 2, "c": [1]}

    with pytest.raises(ValueError):
        dict_to_dataclass(data, Error)


class NoDataclass:
    a: int
    b: str


def test_dict_to_dataclass_special_types():
    data = {"a": 1, "b": "test"}

    with pytest.raises(ValueError):
        dict_to_dataclass(data, NoDataclass)


@dataclass
class WithDataclass:
    value: int
    no_dataclass: NoDataclass


def test_dict_to_dataclass_with_no_dataclass():
    data = {
        "value": 1,
        "no_dataclass": {"a": "adf", "b": "test"},
    }

    with pytest.raises(ValueError):
        dict_to_dataclass(data, WithDataclass)
