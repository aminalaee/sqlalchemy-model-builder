# SQLAlchemy Model Builder
![test](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/test.yml/badge.svg) ![publish](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/publish.yml/badge.svg) [![codecov](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder/branch/main/graph/badge.svg?token=QOLK6R9M52)](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder) 
[![pypi](https://img.shields.io/pypi/v/sqlalchemy-model-builder?color=%2334D058&label=pypi)](https://pypi.org/project/sqlalchemy-model-builder/)

## Features
- Build and Save SQLALchemy models with random data
- Build relationships
- Build minimal (with required) fields only

## How to use
Build SQLAlchemy model:
```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Integer, String, Text

from sqlalchemy_model_builder import ModelBuilder

Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")


class User(Base):
    __tablename__ = "users"

    addresses = relationship("Address", back_populates="user")
    bio = Column(Text)
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


random_user = ModelBuilder(User).build()  # This will not insert the User

minimal_random_user = ModelBuilder(User, minimal=True).build()  # Builds User with `id` and `name`

random_address = ModelBuilder(Address).build(user_id=user.id)  # Build with `user_id`
```

Save SQLAlchemy model:
```
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Integer, String

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
    bio = Column(Text)
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


Base.metadata.create_all(engine)

LocalSession = sessionmaker(bind=engine)

db = LocalSession()


random_user = ModelBuilder(User).save(db=db)  # Builds and Saves model using provided session

random_address = ModelBuilder(Address).save(db=db, user_id=user.id)  # Save with `user_id`
```

## Supported Data Types
- BigInteger
- Boolean
- Date
- DateTime
- Enum  (Todo)
- Float
- Integer
- Interval
- LargeBinary (Todo)
- MatchType (Todo)
- Numeric (Todo)
- PickleType (Todo)
- SchemaType (Todo)
- SmallInteger
- String
- Text
- Time
- Unicode
- UnicodeText
