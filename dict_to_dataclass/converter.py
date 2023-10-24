import datetime
import typing
from dataclasses import is_dataclass
from decimal import Decimal


def is_type_optional(field_type) -> bool:
    field_origin = typing.get_origin(field_type)
    field_args = typing.get_args(field_type)

    return (
        field_origin is typing.Union
        and len(field_args) == 2
        and type(None) in field_args
    )


def convert_std_types(field_type, value) -> typing.Any:
    if field_type == datetime.date and isinstance(value, str):
        return datetime.date.fromisoformat(value)
    elif field_type == datetime.datetime and isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    elif field_type == Decimal and isinstance(value, float):
        # Avoid problems with float to decimal conversion
        return Decimal(repr(value))

    return field_type(value)


def convert_typing_types(field_type_origin, field_type, value) -> typing.Any:
    if is_type_optional(field_type):
        optional_type = typing.get_args(field_type)[0]
        return convert_std_types(optional_type, value)
    elif field_type_origin == list:
        if not isinstance(value, list):
            raise TypeError(f'Value: {value} is not a list. It is a "{type(value)}"')

        list_types = typing.get_args(field_type)
        if len(list_types) != 1:
            raise TypeError("Make sure to define lists like this: list[type]")

        return [convert_std_types(list_types[0], v) for v in value]
    elif field_type_origin == tuple:
        if not isinstance(value, tuple):
            raise TypeError(f'Value: {value} is not a tuple. It is a "{type(value)}"')

        tuple_types = typing.get_args(field_type)
        if len(tuple_types) == 1:
            return tuple(convert_std_types(tuple_types[0], v) for v in value)
    elif field_type_origin == dict:
        if not isinstance(value, dict):
            raise TypeError(f'Value: {value} is not a tuple. It is a "{type(value)}"')

        dict_types = typing.get_args(field_type)
        if len(dict_types) != 2:
            raise TypeError("Make sure to define dicts like this: dict[type, type]")

        return {
            convert_std_types(dict_types[0], k): convert_std_types(dict_types[1], v)
            for k, v in value.items()
        }

    return field_type_origin(value)


T = typing.TypeVar("T")


def dict_to_dataclass(data: dict, dataclass_class: type[T]) -> T:
    import dataclasses

    if not dataclasses.is_dataclass(dataclass_class):
        raise TypeError(f"Provided class: {dataclass_class} is not a dataclass")

    fields_kwargs = {}

    for field in dataclasses.fields(dataclass_class):
        field_name = field.name
        field_type = field.type
        field_type_origin = typing.get_origin(field_type)

        try:
            value = data[field.name]
        except KeyError as ex:
            raise ValueError(f"Field {field_name} not in {data} dict: {ex}")

        try:
            if value is None:
                ...
            elif dataclasses.is_dataclass(field_type):
                value = dict_to_dataclass(value, field_type)
            elif field_type_origin is not None:
                value = convert_typing_types(field_type_origin, field_type, value)
            elif field_type != type(value):
                value = convert_std_types(field_type, value)
        except Exception as ex:
            raise ValueError(
                f'Can not convert data field "{field_name}" with value: '
                f'"{value}" (type: {type(value)}) to dataclass type: "{field_type}": {ex}'
            )

        fields_kwargs[field_name] = value

    return dataclass_class(**fields_kwargs)  # type: ignore[return-value]
