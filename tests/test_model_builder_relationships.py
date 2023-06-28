import pytest
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from sqlalchemy_model_builder import ModelBuilder, ModelBuilderException

Base = declarative_base()
engine = create_engine("sqlite://")
session_maker = sessionmaker(bind=engine)


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")


class User(Base):
    __tablename__ = "users"

    addresses = relationship("Address", back_populates="user")
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


Base.metadata.create_all(engine)


def test_build_model_with_foreign_key():
    ModelBuilder(Address).build()


def test_build_related_model_and_use_in_build():
    user = ModelBuilder(User).build()
    address = ModelBuilder(Address).build(user_id=user.id)

    assert address.user_id == user.id


def test_build_model_with_invalid_attrs_raises_exception():
    with pytest.raises(ModelBuilderException):
        ModelBuilder(User).build(invalid_field="test")


def test_build_related_model_and_use_in_save():
    with session_maker() as session:
        user = ModelBuilder(User).save(session)
        address = ModelBuilder(Address).save(session, user_id=user.id)

        queried_user = session.query(User).get(user.id)
        queried_address = session.query(Address).get(address.id)

    assert user == queried_user
    assert address == queried_address
    assert queried_user.id == address.user_id


def test_save_model_with_foreign_key():
    with session_maker() as session:
        address = ModelBuilder(Address).save(session)

        queried_address = session.query(Address).get(address.id)
        queried_user = session.query(User).get(address.user_id)

    assert address == queried_address
    assert queried_user is not None
