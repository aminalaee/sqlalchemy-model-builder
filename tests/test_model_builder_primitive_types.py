import unittest

from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        Integer, Interval, LargeBinary, SmallInteger, String,
                        Text, Time, Unicode, UnicodeText, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy_model_builder import ModelBuilder, ModelBuilderException

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)


class User(Base):
    __tablename__ = "users"

    active_until = Column(Interval)
    bio = Column(Text)
    bio_unicode = Column(UnicodeText)
    image = Column(LargeBinary)
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    name = Column(String, nullable=False)
    name_unicode = Column(Unicode)
    joined_at = Column(DateTime)
    date_of_birth = Column(Date)
    time_of_birth = Column(Time)
    deposit = Column(Float)
    points = Column(SmallInteger)
    profile_visits = Column(BigInteger)

Base.metadata.create_all(engine)

LocalSession = sessionmaker(bind=engine)

db: Session = LocalSession()


class TestModelBuilderPrimitiveTypes(unittest.TestCase):
    def test_build_model_with_invalid_class_throws_exception(self):
        with self.assertRaises(ModelBuilderException):
            ModelBuilder(Base).build()

    def test_build_model_with_primitive_types(self):
        ModelBuilder(User).build()

    def test_build_model_with_primitive_types_with_minimal(self):
        user = ModelBuilder(User, minimal=True).build()

        self.assertFalse(user.bio)

    def test_save_model_with_primitive_types(self):
        user = ModelBuilder(User).save(db=db)
        queried_user = db.query(User).get(user.id)

        self.assertEqual(user, queried_user)
