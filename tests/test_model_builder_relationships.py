import unittest

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

from sqlalchemy_model_builder import ModelBuilder

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)


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

LocalSession = sessionmaker(bind=engine)

db: Session = LocalSession()


class TestModelBuilderPrimitiveTypes(unittest.TestCase):
    def test_build_model_with_foreign_key(self):
        ModelBuilder(Address).build()

    def test_build_related_model_and_use_in_build(self):
        pass

    def test_build_related_model_and_use_in_save(self):
        pass

    def test_save_model_with_foreign_key(self):
        ModelBuilder(Address).save(db=db)
