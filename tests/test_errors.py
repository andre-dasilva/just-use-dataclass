from dataclasses import dataclass

import pytest

from dict_to_dataclass import dict_to_dataclass


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
