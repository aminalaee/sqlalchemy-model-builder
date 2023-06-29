# SQLAlchemy Model Builder
![test](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/test.yml/badge.svg) ![publish](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/publish.yml/badge.svg) [![codecov](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder/branch/main/graph/badge.svg?token=QOLK6R9M52)](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder) 
[![pypi](https://img.shields.io/pypi/v/sqlalchemy-model-builder?color=%2334D058&label=pypi)](https://pypi.org/project/sqlalchemy-model-builder/)

## Features
- Build SQLAlchemy model instance with random data
- Save SQLAlchemy model instance with random data
- Build relationships
- Build minimal (with required fields) only

---

## Installation

```shell
$ pip install sqlalchemy-model-builder
```

---

## How to use
Deinfe the SQLAlchemy models:

```python
from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

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

```

Save random model instance:

```python
from sqlalchemy_model_builder import ModelBuilder

random_user = ModelBuilder(User).save(db)
```

Build random model without saving:

```python
random_user = ModelBuilder(User).build()
```

Build minimal model instance:

```python
minimal_random_user = ModelBuilder(User, minimal=True).build()
```

Build or save with specific values:

```python
random_address = ModelBuilder(Address).build(user_id=1)
```

---

## Supported Data Types
- BigInteger
- Boolean
- Date
- DateTime
- Enum
- Float
- Integer
- Interval
- LargeBinary
- MatchType (Todo)
- Numeric
- PickleType (Todo)
- SchemaType (Todo)
- SmallInteger
- String
- Text
- Time
- Unicode
- UnicodeText
