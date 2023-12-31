# just-use-dataclass

[![Tests](https://github.com/andre-dasilva/just-use-dataclass/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/andre-dasilva/just-use-dataclass/actions/workflows/tests.yaml)

Simple function to convert a python dict to a dataclass.

If you want to know how the library works, the best place to look at is in the [tests](./tests)

In short: it converts a dictionary to a dataclass by looking at the type annotations in the dataclass and converting the data in the dictionary to it.

The library has no dependencies. Its just the python standard library. Which sometimes is all you need :-)

For more advanced data conversion (or even validation) take a look at [pydantic](https://github.com/pydantic/pydantic) or [attrs](https://github.com/python-attrs/attrs)

## Installation

```
pip install just-use-dataclass
```

## Usage and examples

### Simple data type conversion

```python
from dataclasses import dataclass
import typing

from just_use_dataclass import dict_to_dataclass

@dataclass
class Simple:
    a: str
    b: int
    c: float
    d: bool
    e: typing.Optional[str]
    f: typing.Optional[str]

data = {
    "a": 1,
    "b": "1",
    "c": "2.0",
    "d": True,
    "e": None,
    "f": 42,
}

simple = dict_to_dataclass(data, Simple)

print(simple)

# Output:
# Simple(a='1', b=1, c=2.0, d=True, e=None, f='42')
```

### Nested dataclass conversion

```python
from dataclasses import dataclass
from decimal import Decimal

from just_use_dataclass import dict_to_dataclass

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

print(nested)

# Output:
# A(value_1=Decimal('23.23'), value_2=Decimal('49.0001'), b=B(value=1, c=C(value='test'))
```

### Deeply nested typing conversion

```python
from dataclasses import dataclass
import typing

from just_use_dataclass import dict_to_dataclass

@dataclass
class Crazy:
    value: dict[str, dict[int, list[typing.Optional[str]]]]

data = {"value": {"test": {1: ["hey", None, 42]}}}

crazy = dict_to_dataclass(data, Crazy)

print(crazy)

# Output:
# Crazy(value={'test': {1: ['hey', None, '42']}})
```

## Contribute

Any pull requests or issues are welcomed. If you want to contribute you can follow these steps:

Just make sure to **include tests** in your PR, if you made a code adjustment

1. Fork and clone the repo

2. Install poetry or just pytest, mypy and black

```sh
poetry install

# or

pip install -U pytest mypy black
```

3. Run tests

```sh
poetry run pytest .
```

3. Linting / Formatting

```sh
poetry run mypy .
poetry run black .
```
