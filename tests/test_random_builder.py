from datetime import date, datetime, time, timedelta, timezone
from enum import Enum
from uuid import UUID

from sqlalchemy_model_builder.random_builder import RandomBuilder


def test_next_date():
    random_date = RandomBuilder.next_date()

    assert isinstance(random_date, date)
    assert random_date.year >= 2000
    assert random_date.year <= 2050


def test_next_datetime():
    random_datetime = RandomBuilder.next_datetime()

    assert isinstance(random_datetime, datetime)
    assert random_datetime.year >= 2000
    assert random_datetime.year <= 2050


def test_next_datetime_utc():
    random_datetime = RandomBuilder.next_datetime_utc()

    assert random_datetime.tzinfo == timezone.utc
    assert isinstance(random_datetime, datetime)
    assert random_datetime.year >= 2000
    assert random_datetime.year <= 2050


def test_next_time():
    random_time = RandomBuilder.next_time()

    assert isinstance(random_time, time)


def test_next_timedelta():
    random_timedelta = RandomBuilder.next_timedelta()

    assert isinstance(random_timedelta, timedelta)
    assert random_timedelta.days <= 7


def test_next_float():
    random_float = RandomBuilder.next_float(maximum=1000)

    assert isinstance(random_float, float)
    assert random_float <= 1000


def test_next_int():
    random_int = RandomBuilder.next_int()

    assert isinstance(random_int, int)
    assert random_int <= 2147483647


def test_next_int64():
    random_int = RandomBuilder.next_int64()

    assert isinstance(random_int, int)
    assert random_int <= 9223372036854775807


def test_next_bool():
    random_bool = RandomBuilder.next_bool()
    assert isinstance(random_bool, bool)


def test_next_enum():
    class Color(Enum):
        RED = 1
        BLUE = 2

    random_enum = RandomBuilder.next_enum(Color)
    assert isinstance(random_enum, int)


def test_next_uuid():
    random_uuid = RandomBuilder.next_uuid()
    assert isinstance(random_uuid, UUID)


def test_next_bytes():
    random_bytes = RandomBuilder.next_bytes(length=100)
    assert len(random_bytes) == 100


def test_next_str():
    random_str = RandomBuilder.next_str(length=64)

    assert isinstance(random_str, str)
    assert len(random_str) == 64
