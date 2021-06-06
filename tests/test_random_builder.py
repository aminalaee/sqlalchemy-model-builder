import unittest
from datetime import date, datetime, time, timedelta, timezone
from uuid import UUID

from sqlalchemy_model_builder.random_builder import RandomBuilder


class TestDateBuilders(unittest.TestCase):
    def test_next_bool_valid_type(self):
        random_bool = RandomBuilder.next_bool()
        self.assertIsInstance(random_bool, bool)

    def test_next_float_valid_type(self):
        random_float = RandomBuilder.next_float()
        self.assertIsInstance(random_float, float)

    def test_next_float_valid_range(self):
        random_float = RandomBuilder.next_float(maximum=1000)
        self.assertLessEqual(random_float, 1000)

    def test_next_date_valid_type(self):
        random_date = RandomBuilder.next_date()
        self.assertIsInstance(random_date, date)

    def test_next_date_valid_range(self):
        random_date = RandomBuilder.next_date()
        self.assertGreaterEqual(random_date.year, 2000)
        self.assertLessEqual(random_date.year, 2050)

    def test_next_datetime_valid_type(self):
        random_datetime = RandomBuilder.next_datetime()
        self.assertIsInstance(random_datetime, datetime)

    def test_next_datetime_valid_range(self):
        random_datetime = RandomBuilder.next_datetime()
        self.assertGreaterEqual(random_datetime.year, 2000)
        self.assertLessEqual(random_datetime.year, 2050)

    def test_next_datetime_utc_valid_type(self):
        random_datetime = RandomBuilder.next_datetime_utc()
        self.assertIsInstance(random_datetime, datetime)

    def test_next_datetime_utc_valid_range(self):
        random_datetime = RandomBuilder.next_datetime_utc()
        self.assertEqual(random_datetime.tzinfo, timezone.utc)
        self.assertGreaterEqual(random_datetime.year, 2000)
        self.assertLessEqual(random_datetime.year, 2050)

    def test_next_int_valid_type(self):
        random_int = RandomBuilder.next_int()
        self.assertIsInstance(random_int, int)

    def test_next_int_valid_range(self):
        random_int = RandomBuilder.next_int()
        self.assertLessEqual(random_int, 2147483647)

    def test_next_int64_valid_type(self):
        random_int = RandomBuilder.next_int64()
        self.assertIsInstance(random_int, int)

    def test_next_int64_valid_range(self):
        random_int = RandomBuilder.next_int64()
        self.assertLessEqual(random_int, 9223372036854775807)

    def test_next_str_valid_type(self):
        random_str = RandomBuilder.next_str()
        self.assertIsInstance(random_str, str)

    def test_next_str_valid_length(self):
        random_str = RandomBuilder.next_str(length=64)
        self.assertLessEqual(len(random_str), 64)

    def test_next_time_valid_type(self):
        random_time = RandomBuilder.next_time()
        self.assertIsInstance(random_time, time)

    def test_next_timedelta_valid_type(self):
        random_timedelta = RandomBuilder.next_timedelta()
        self.assertIsInstance(random_timedelta, timedelta)

    def test_next_timedelta_valid_range(self):
        random_timedelta = RandomBuilder.next_timedelta()
        self.assertLessEqual(random_timedelta.days, 7)

    def test_next_uuid_valid_type(self):
        random_uuid = RandomBuilder.next_uuid()
        self.assertIsInstance(random_uuid, UUID)
