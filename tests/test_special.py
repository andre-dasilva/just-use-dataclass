import datetime
from dataclasses import dataclass

from dict_to_dataclass import dict_to_dataclass


@dataclass
class Times:
    birthday: datetime.date
    birthday_str: datetime.date
    timestamp: datetime.datetime
    timestamp_str: datetime.datetime
    time: datetime.time
    time_str: datetime.time


@dataclass
class Special:
    value: str
    times: Times


def test_dict_to_dataclass_special_types():
    data = {
        "value": datetime.date(2012, 12, 3),
        "times": {
            "birthday": datetime.date(1993, 3, 12),
            "birthday_str": "1993-03-12",
            "timestamp": datetime.datetime(1988, 11, 2, 20, 30, 40),
            "timestamp_str": "1988-11-02T20:30:40",
            "time": datetime.time(20, 30, 40),
            "time_str": "20:30:40",
        },
    }

    special = dict_to_dataclass(data, Special)

    assert isinstance(special.value, str)
    assert special.value == "2012-12-03"

    assert isinstance(special.times, Times)

    assert isinstance(special.times.birthday, datetime.date)
    assert special.times.birthday == datetime.date(1993, 3, 12)
    assert isinstance(special.times.birthday_str, datetime.date)
    assert special.times.birthday_str == datetime.date(1993, 3, 12)

    assert isinstance(special.times.timestamp, datetime.datetime)
    assert special.times.timestamp == datetime.datetime(1988, 11, 2, 20, 30, 40)
    assert isinstance(special.times.timestamp_str, datetime.datetime)
    assert special.times.timestamp == datetime.datetime(1988, 11, 2, 20, 30, 40)

    assert isinstance(special.times.time, datetime.time)
    assert special.times.time == datetime.time(20, 30, 40)
    assert isinstance(special.times.time_str, datetime.time)
    assert special.times.time_str == datetime.time(20, 30, 40)
