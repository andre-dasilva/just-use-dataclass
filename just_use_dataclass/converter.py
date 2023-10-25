import dataclasses
import datetime
import typing
from decimal import Decimal


def is_type_optional(field_type) -> bool:
    field_origin = typing.get_origin(field_type)
    field_args = typing.get_args(field_type)

    return (
        field_origin is typing.Union
        and len(field_args) == 2
        and field_args[1] is type(None)
    )


def convert_std_types(field_type, value) -> typing.Any:
    if field_type == datetime.date and isinstance(value, str):
        # Python 3.11 allows for time zones in fromisoformat(),
        # for older versions we would need a dependency (like python-dateutil)
        return datetime.date.fromisoformat(value)
    elif field_type == datetime.datetime and isinstance(value, str):
        # Python 3.11 allows for time zones in fromisoformat(),
        # for older versions we would need a dependency (like python-dateutil)
        return datetime.datetime.fromisoformat(value)
    elif field_type == datetime.time and isinstance(value, str):
        # Python 3.11 allows for time zones in fromisoformat(),
        # for older versions we would need a dependency (like python-dateutil)
        return datetime.time.fromisoformat(value)
    elif field_type == Decimal and isinstance(value, float):
        # Avoid problems with float to decimal conversion
        return Decimal(repr(value))

    return field_type(value)


def convert_list_types(field_type, value):
    if not isinstance(value, list):
        raise TypeError(f'Value: {value} is not a list. It is a "{type(value)}"')

    list_types = typing.get_args(field_type)
    if len(list_types) != 1:
        raise TypeError("Make sure to define lists like this: list[type]")

    return [convert_types(list_types[0], v) for v in value]


def convert_tuple_types(field_type, value):
    if not isinstance(value, tuple):
        raise TypeError(f'Value: {value} is not a tuple. It is a "{type(value)}"')

    tuple_types = typing.get_args(field_type)
    if len(tuple_types) == 1:
        return tuple(convert_types(tuple_types[0], v) for v in value)


def convert_dict_types(field_type, value):
    if not isinstance(value, dict):
        raise TypeError(f'Value: {value} is not a tuple. It is a "{type(value)}"')

    dict_types = typing.get_args(field_type)
    if len(dict_types) != 2:
        raise TypeError("Make sure to define dicts like this: dict[type, type]")

    return {
        convert_types(dict_types[0], k): convert_types(dict_types[1], v)
        for k, v in value.items()
    }


def convert_types(field_type, value) -> typing.Any:
    field_type_origin = typing.get_origin(field_type)

    if value is None or field_type is type(value):
        return value
    elif is_type_optional(field_type):
        optional_type = typing.get_args(field_type)[0]
        return convert_types(optional_type, value)
    elif field_type_origin is list:
        return convert_list_types(field_type, value)
    elif field_type_origin is tuple:
        return convert_tuple_types(field_type, value)
    elif field_type_origin is dict:
        return convert_dict_types(field_type, value)
    elif field_type_origin is typing.Union:
        raise NotImplementedError("Unions are not supported")

    return convert_std_types(field_type, value)


T = typing.TypeVar("T")


def dict_to_dataclass(data: dict, dataclass_class: type[T]) -> T:
    if not dataclasses.is_dataclass(dataclass_class):
        raise TypeError(f"Provided class: {dataclass_class} is not a dataclass")

    fields_kwargs = {}

    for field in dataclasses.fields(dataclass_class):
        field_name = field.name

        try:
            value = data[field_name]
        except KeyError as ex:
            raise ValueError(f"Field {field_name} not in {data} dict: {ex}")

        field_type = field.type

        try:
            if dataclasses.is_dataclass(field_type):
                value = dict_to_dataclass(value, field_type)
            else:
                value = convert_types(field_type, value)
        except Exception as ex:
            raise ValueError(
                f'Can not convert data field "{field_name}" with value: '
                f'"{value}" (type: {type(value)}) to dataclass type: "{field_type}": {ex}'
            )

        fields_kwargs[field_name] = value

    return dataclass_class(**fields_kwargs)  # type: ignore[return-value]
