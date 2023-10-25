# just-use-dataclass

Simple function to convert a python dict to a dataclass.

If you want to know how the library works, the best place to look at is in the [tests](./tests)

In short: it converts a dictionary to a dataclass by looking at the annotations in the dataclass and converting the
data in the dictionary to it.

## Installation

1. Fork and clone the repo

2. Install poetry

```sh
poetry install
```

3. Run tests

```sh
poetry shell
pytest
```

## Use in production

The library is really new. if you want to contribute feel welcome.
Otherwise don't use it in production (yet) :)
