from dataclasses import dataclass

import pytest

from just_use_dataclass import dict_to_dataclass


@dataclass
class Error:
    a: int
    b: str


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
