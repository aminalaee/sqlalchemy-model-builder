import enum
import random
import string
import uuid
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, List, Type


class RandomBuilder:
    @classmethod
    def next_bool(cls) -> bool:
        return random.choice([True, False])

    @classmethod
    def next_bytes(cls, length: int = 8) -> bytes:
        return random.getrandbits(length * 8).to_bytes(length, "little")

    @classmethod
    def next_date(cls) -> date:
        return date(
            year=random.randint(2000, 2050),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
        )

    @classmethod
    def next_datetime(cls) -> datetime:
        return datetime(
            year=random.randint(2000, 2050),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59),
        )

    @classmethod
    def next_datetime_utc(cls) -> datetime:
        return cls.next_datetime().astimezone(timezone.utc)

    @classmethod
    def next_enum(cls, e: Type[enum.Enum]) -> Any:
        return random.choice([item.value for item in e])

    @classmethod
    def next_float(
        cls, minimum: float = 0, maximum: float = 2147483647, precision: int = 5
    ) -> float:
        return round(random.uniform(minimum, maximum), precision)

    @classmethod
    def next_from_list(cls, seq: List[Any]) -> Any:
        return random.choice(seq)

    @classmethod
    def next_int(cls, minimum: int = 0, maximum: int = 2147483647) -> int:
        return random.randint(minimum, maximum)

    @classmethod
    def next_int64(cls, minimum: int = 0, maximum: int = 9223372036854775807) -> int:
        return random.randint(minimum, maximum)

    @classmethod
    def next_str(cls, length: int = 16) -> str:
        return "".join(random.choice(string.ascii_letters) for _ in range(length))

    @classmethod
    def next_time(cls) -> time:
        return time(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59),
        )

    @classmethod
    def next_timedelta(cls) -> timedelta:
        return timedelta(
            days=random.randint(1, 7),
            hours=random.randint(1, 23),
            minutes=random.randint(0, 59),
        )

    @classmethod
    def next_uuid(cls) -> uuid.UUID:
        return uuid.uuid4()
