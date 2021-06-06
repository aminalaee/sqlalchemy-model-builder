import random
import string
import uuid
from datetime import date, datetime, time, timedelta, timezone


class RandomBuilder:
    @classmethod
    def next_bool(cls) -> bool:
        return random.choice([True, False])

    @classmethod
    def next_date(cls) -> date:
        return date(year=random.randint(2000, 2050), month=random.randint(1, 12), day=random.randint(1, 28))

    @classmethod
    def next_datetime(cls) -> datetime:
        return datetime(
            year=random.randint(2000, 2050),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59))

    @classmethod
    def next_datetime_utc(cls) -> datetime:
        return cls.next_datetime().astimezone(timezone.utc)

    @classmethod
    def next_float(cls, minimum=0, maximum=2147483647, precision=5) -> float:
        return round(random.uniform(minimum, maximum), precision)

    @classmethod
    def next_int(cls, minimum=0, maximum=2147483647) -> int:
        return random.randint(minimum, maximum)

    @classmethod
    def next_int64(cls, minimum=0, maximum=9223372036854775807) -> int:
        return random.randint(minimum, maximum)

    @classmethod
    def next_str(cls, length=16) -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @classmethod
    def next_time(cls) -> time:
        return time(hour=random.randint(0, 23), minute=random.randint(0, 59), second=random.randint(0, 59))

    @classmethod
    def next_timedelta(cls) -> timedelta:
        return timedelta(days=random.randint(1, 7), hours=random.randint(1, 23), minutes=random.randint(0, 59))

    @classmethod
    def next_uuid(cls) -> uuid.UUID:
        return uuid.uuid4()
