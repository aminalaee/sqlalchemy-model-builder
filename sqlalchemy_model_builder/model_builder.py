from datetime import date, datetime, time, timedelta
from typing import Any, Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.orm import Mapper, Session

from sqlalchemy_model_builder._models import ColumnValuePair, ColumnValuePairList
from sqlalchemy_model_builder.exceptions import ModelBuilderException
from sqlalchemy_model_builder.random_builder import RandomBuilder

T = TypeVar("T")

_TYPE_MAPPING = {
    "BigInteger": RandomBuilder.next_int,
    "Boolean": RandomBuilder.next_bool,
    "Date": RandomBuilder.next_date,
    "DateTime": RandomBuilder.next_datetime,
    "Float": RandomBuilder.next_float,
    "Integer": RandomBuilder.next_int,
    "Interval": RandomBuilder.next_timedelta,
    "LargeBinary": RandomBuilder.next_bytes,
    "Numeric": RandomBuilder.next_float,
    "String": RandomBuilder.next_str,
    "Text": RandomBuilder.next_str,
    "Time": RandomBuilder.next_time,
    "Unicode": RandomBuilder.next_str,
    "UnicodeText": RandomBuilder.next_str,
    "Uuid": RandomBuilder.next_uuid,
}


class ModelBuilder(Generic[T]):
    def __init__(self, db_model: Type[T], minimal: bool = False):
        self.db: Optional[Session] = None
        self.db_model = db_model
        self.minimal = minimal

    def build(self, **attrs: Any) -> T:
        """Build SQLAlchemy model with random data and
        return it without persisting into database.

        :returns: a SQLAlchemy database model with generated random data
        :rtype: Any
        """
        try:
            column_values = self.__get_model_fields(self.db_model)
        except NoInspectionAvailable as sqlalchemy_exception:
            raise ModelBuilderException(
                f"Class {self.db_model} is not a SQLAlchemy model"
            ) from sqlalchemy_exception

        column_values_with_attrs = dict(column_values.to_dict(), **attrs)

        try:
            instance = self.db_model(**column_values_with_attrs)
        except TypeError as sqlalchemy_exception:
            raise ModelBuilderException(
                f"Invalid fields for model: {self.db_model}"
            ) from sqlalchemy_exception

        return instance

    def save(self, db: Session, **attrs: Any) -> T:
        """Build SQLAlchemy model with random data and
        persist it into database using provided db.

        :param db: SQLAlchemy database session
        :type db: Session
        :returns: a SQLAlchemy database model with generated random data
        :rtype: Any
        """
        self.db = db

        instance = self.build(**attrs)

        self.__save(instance)

        return instance

    def __build_model_relationships(self, mapper: Mapper) -> ColumnValuePairList:
        """Build model relationships

        :param mapper: Mapper to load relationship from
        :type mapper: SQLAlchemy ORM Mapper
        :returns: a List of ColumnValuePair to map column with instance
        :rtype: ColumnValuePairList
        """
        related_models = []

        for relationship in mapper.relationships:
            foreign_keys = any(c.foreign_keys for c in relationship.local_columns)
            if not foreign_keys:
                continue

            values = self.__get_model_fields(relationship.mapper.class_)
            instance = relationship.mapper.class_(**values.to_dict())

            if self.db:
                self.__save(instance)

            foreign_key_column = next(iter(relationship.local_columns))

            column_value = ColumnValuePair(foreign_key_column.name, instance)
            related_models.append(column_value)

        return ColumnValuePairList(related_models)

    def __get_model_fields(self, db_model: Type) -> ColumnValuePairList:
        """Get model field and values from SQLAlchemy model

        :returns: a dictionary of model field attribute and values.
        :rtype: ColumnValuePairList
        """
        column_values = []
        mapper = inspect(db_model)

        relationships = self.__build_model_relationships(mapper)  # type: ignore
        for relationship in relationships.pairs:
            primary_key = inspect(relationship.value).mapper.primary_key[0]
            column_value = ColumnValuePair(
                relationship.column, getattr(relationship.value, primary_key.key)
            )
            column_values.append(column_value)

        for column in mapper.columns:  # type: ignore
            type_ = column.type.__class__.__name__

            if self.minimal and column.nullable:
                continue

            if column.foreign_keys:
                continue

            if type_ == "Enum":
                random_value = RandomBuilder.next_from_list(column.type.enums)
            else:
                builder = _TYPE_MAPPING.get(type_, RandomBuilder.next_str)
                random_value = builder()

            column_value = ColumnValuePair(column.key, random_value)
            column_values.append(column_value)

        return ColumnValuePairList(column_values)

    def __save(self, instance: T) -> None:
        assert self.db is not None

        self.db.add(instance)
        self.db.commit()
