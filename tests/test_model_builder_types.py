import enum
import unittest

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
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy_model_builder import ModelBuilder, ModelBuilderException

Base = declarative_base()

engine = create_engine("sqlite://")


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

LocalSession = sessionmaker(bind=engine)

db: Session = LocalSession()


class TestModelBuilderTypes(unittest.TestCase):
    def test_build_model_with_invalid_class_throws_exception(self):
        with self.assertRaises(ModelBuilderException):
            ModelBuilder(Base).build()

    def test_build_model_types(self):
        ModelBuilder(User).build()

    def test_build_model_minimal(self):
        user = ModelBuilder(User, minimal=True).build()

        self.assertFalse(user.bio)

    def test_save_model_types(self):
        user = ModelBuilder(User).save(db=db)
        queried_user = db.query(User).get(user.id)

        self.assertEqual(user, queried_user)

    def test_build_multiple_models_not_duplicate(self):
        user_1 = ModelBuilder(User).save(db=db)
        user_2 = ModelBuilder(User).save(db=db)

        self.assertNotEqual(user_1.id, user_2.id)
        self.assertNotEqual(user_1.bio, user_2.bio)
        self.assertNotEqual(user_1.uuid, user_2.uuid)
        self.assertNotEqual(user_1.date_of_birth, user_2.date_of_birth)
