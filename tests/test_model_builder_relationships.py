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
        user = ModelBuilder(User).build()
        address = ModelBuilder(Address).build(user_id=user.id)

        self.assertEqual(address.user_id, user.id)

    def test_build_related_model_and_use_in_save(self):
        user = ModelBuilder(User).save(db=db)
        address = ModelBuilder(Address).save(db=db, user_id=user.id)

        queried_user = db.query(User).get(user.id)
        queried_address = db.query(Address).get(address.id)

        self.assertEqual(user, queried_user)
        self.assertEqual(address, queried_address)
        self.assertEqual(queried_address.user_id, address.user_id)

    def test_save_model_with_foreign_key(self):
        address = ModelBuilder(Address).save(db=db)

        queried_address = db.query(Address).get(address.id)
        queried_user = db.query(User).get(address.user_id)

        self.assertEqual(address, queried_address)
        self.assertTrue(queried_user)
