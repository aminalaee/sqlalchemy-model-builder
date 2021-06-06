# SQLAlchemy Model Builder
![test](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/test.yml/badge.svg) ![publish](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/publish.yml/badge.svg) [![codecov](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder/branch/main/graph/badge.svg?token=QOLK6R9M52)](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder) 
[![pypi](https://img.shields.io/pypi/v/sqlalchemy-model-builder?color=%2334D058&label=pypi)](https://pypi.org/project/sqlalchemy-model-builder/)

## Features
- Build and Save SQLALchemy models with random data
- Build relationships (Todo)
- Build with minimal(required) fields only (Todo)

## How to use
Build SQLAlchemy model:
```
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_model_builder import ModelBuilder

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    bio = Column(Text)
    id = Column(Integer, primary_key=True)
    name = Column(String)


random_user = ModelBuilder(User).build()  # Note: This will not insert the User, you have to do it manually
```

Save SQLAlchemy model:
```
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_model_builder import ModelBuilder

Base = declarative_base()

engine = create_engine("sqlite://", echo=True)


class User(Base):
    __tablename__ = "users"

    bio = Column(Text)
    id = Column(Integer, primary_key=True)
    name = Column(String)


Base.metadata.create_all(engine)

LocalSession = sessionmaker(bind=engine)

db = LocalSession()


random_user = ModelBuilder(User).save(db=db)  # Note: Build and Save model using provided session
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
