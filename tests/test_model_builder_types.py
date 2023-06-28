import enum
from datetime import date, datetime, time, timedelta
from uuid import UUID

import pytest
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    Interval,
    LargeBinary,
    Numeric,
    SmallInteger,
    String,
    Text,
    Time,
    Unicode,
    UnicodeText,
    Uuid,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy_model_builder import ModelBuilder, ModelBuilderException

Base = declarative_base()
engine = create_engine("sqlite://")
session_maker = sessionmaker(bind=engine)


class StatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"

    active_until = Column(Interval)
    bio = Column(Text)
    bio_unicode = Column(UnicodeText)
    date_of_birth = Column(Date)
    deposit = Column(Float)
    id = Column(Integer, primary_key=True)
    image = Column(LargeBinary)
    is_active = Column(Boolean)
    joined_at = Column(DateTime)
    name = Column(String, nullable=False)
    name_unicode = Column(Unicode)
    points = Column(SmallInteger)
    profile_visits = Column(BigInteger)
    rank = Column(Numeric(precision=8, asdecimal=False, decimal_return_scale=None))
    status = Column(Enum(StatusEnum), default=StatusEnum.active)
    time_of_birth = Column(Time)
    uuid = Column(Uuid)


Base.metadata.create_all(engine)


def test_build_model_with_invalid_class_throws_exception():
    with pytest.raises(ModelBuilderException):
        ModelBuilder(Base).build()


def test_build_model_types():
    user = ModelBuilder(User).build()

    assert isinstance(user, User)
    assert isinstance(user.active_until, timedelta)
    assert isinstance(user.bio, str)
    assert isinstance(user.bio_unicode, str)
    assert isinstance(user.date_of_birth, date)
    assert isinstance(user.deposit, float)
    assert isinstance(user.id, int)
    assert isinstance(user.image, bytes)
    assert isinstance(user.is_active, bool)
    assert isinstance(user.joined_at, datetime)
    assert isinstance(user.name, str)
    assert isinstance(user.name_unicode, str)
    assert isinstance(user.points, int)
    assert isinstance(user.profile_visits, int)
    assert isinstance(user.rank, float)
    assert isinstance(user.status, str)
    assert isinstance(user.time_of_birth, time)
    assert isinstance(user.uuid, UUID)


def test_build_model_minimal():
    user = ModelBuilder(User, minimal=True).build()

    assert user.bio is None


def test_save_model_types():
    with session_maker() as session:
        user = ModelBuilder(User).save(session)
        queried_user = session.query(User).get(user.id)

    assert user == queried_user


def test_build_multiple_models_not_duplicate():
    with session_maker(expire_on_commit=False) as session:
        user_1 = ModelBuilder(User).save(session)
        user_2 = ModelBuilder(User).save(session)

    assert user_1 != user_2
    assert user_1.id != user_2.id
    assert user_1.bio != user_2.bio
    assert user_1.uuid != user_2.uuid
    assert user_1.date_of_birth != user_2.date_of_birth
