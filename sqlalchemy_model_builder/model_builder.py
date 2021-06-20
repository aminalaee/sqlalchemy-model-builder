from datetime import date, datetime, time, timedelta
from typing import Any, Callable, Optional, Type

from sqlalchemy import inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.orm.session import Session

from sqlalchemy_model_builder.exceptions import ModelBuilderException
from sqlalchemy_model_builder.models import (ColumnValuePair,
                                             ColumnValuePairList)
from sqlalchemy_model_builder.random_builder import RandomBuilder


class ModelBuilder:
    def __init__(self, db_model: Type, minimal: bool = False):
        self.db: Optional[Session] = None
        self.db_model: Type = db_model
        self.minimal: bool = minimal

    def build(self, **attrs) -> Any:
        """Build SQLAlchemy model with random data and return it without persisting into database

        :returns: a SQLAlchemy database model with generated random data
        :rtype: Any
        """
        try:
            column_values = self.__get_model_fields(self.db_model)
        except NoInspectionAvailable as sqlalchemy_exception:
            raise ModelBuilderException(f"Class {self.db_model} is not a SQLAlchemy model") from sqlalchemy_exception

        column_values_with_attrs = dict(column_values.to_dict(), **attrs)

        try:
            instance = self.db_model(**column_values_with_attrs)
        except TypeError as sqlalchemy_exception:
            raise ModelBuilderException(f"Invalid fields for model: {self.db_model}") from sqlalchemy_exception

        return instance

    def save(self, db: Session, **attrs) -> Any:
        """Build SQLAlchemy model with random data and persist it into database using provided db

        :param db: SQLAlchemy database session
        :type db: Session
        :returns: a SQLAlchemy database model with generated random data
        :rtype: Any
        """
        self.db = db

        instance = self.build(**attrs)

        self.__save(instance)

        return instance

    def __build_model_relationships(self, mapper) -> ColumnValuePairList:
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

            values = self.__get_model_fields(relationship.mapper)
            instance = relationship.mapper.class_(**values.to_dict())

            if self.db:
                self.__save(instance)

            foreign_key_column = next(iter(relationship.local_columns))

            column_value = ColumnValuePair(foreign_key_column.key, instance)
            related_models.append(column_value)

        return ColumnValuePairList(related_models)

    def __get_model_fields(self, db_model: Type) -> ColumnValuePairList:
        """Get model field and values from SQLAlchemy model

        :returns: a dictionary of model field values; key is name of field and value is random value
        :rtype: ColumnValuePairList
        """
        column_values = []
        mapper = inspect(db_model)

        relationships = self.__build_model_relationships(mapper)
        for relationship in relationships.pairs:
            primary_key = inspect(relationship.value).mapper.primary_key[0]
            column_value = ColumnValuePair(relationship.column, getattr(relationship.value, primary_key.key))
            column_values.append(column_value)

        for column in mapper.columns:
            python_type: Optional[type] = None

            if hasattr(column.type, "impl"):
                if hasattr(column.type.impl, "python_type"):
                    python_type = column.type.python_type
            elif hasattr(column.type, "python_type"):
                python_type = column.type.python_type
            assert python_type, f"Could not infer python_type for {column}"

            if self.minimal and column.nullable:
                continue

            if column.foreign_keys:
                continue

            random_value = self.__map_field_to_random_builder_method(python_type)()
            column_value = ColumnValuePair(column.key, random_value)
            column_values.append(column_value)

        return ColumnValuePairList(column_values)

    def __map_field_to_random_builder_method(self, field_type: type) -> Callable[[], Any]:
        """Mapping between field type and RandomBuilder methods

        :returns: a RandomBuilder method for the provided type
        :rtype: function
        """
        func: Callable[[], Any] = RandomBuilder.next_str

        if field_type == bool:
            func = RandomBuilder.next_bool
        elif field_type == date:
            func = RandomBuilder.next_date
        elif field_type == datetime:
            func = RandomBuilder.next_datetime
        elif field_type == float:
            func = RandomBuilder.next_float
        elif field_type == int:
            func = RandomBuilder.next_int
        elif field_type == str:
            func = RandomBuilder.next_str
        elif field_type == time:
            func = RandomBuilder.next_time
        elif field_type == timedelta:
            func = RandomBuilder.next_timedelta

        return func

    def __save(self, instance: Any):
        assert self.db is not None

        self.db.add(instance)
        self.db.commit()
