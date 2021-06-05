from datetime import date, datetime, time, timedelta
from typing import Any, Callable, Dict, Optional, Type

from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.session import Session

from sqlalchemy_model_builder.exceptions import ModelBuilderException
from sqlalchemy_model_builder.random_builder import RandomBuilder


class ModelBuilder:
    def __init__(self, db_model: Type):
        self.db_model: Type = db_model
        self.field_types: Dict[str, Type] = {}
        self.field_values: Dict[str, Any] = {}

    def build(self) -> Any:
        """Build SQLAlchemy model with random data and return it without persisting into database

        :returns: a SQLAlchemy database model with generated random data
        :rtype: Any
        """
        try:
            self.field_types = self.__get_model_fields()
        except NoInspectionAvailable as sqlalchemy_exception:
            raise ModelBuilderException(f"Class {self.db_model} is not a SQLAlchemy model") from sqlalchemy_exception

        self.field_values = self.__get_model_field_values()

        instance = self.db_model(**self.field_values)

        return instance

    def save(self, db: Session) -> Any:
        """Build SQLAlchemy model with random data and persist it into database using provided db

        :param db: SQLAlchemy database session
        :type db: Session
        :returns: a SQLAlchemy database model with generated random data
        :rtype: Any
        """
        instance = self.build()

        db.add(instance)
        db.commit()

        return instance

    def __get_model_fields(self) -> Dict[str, Type]:
        """Extract model field types from SQLAlchemy model

        :returns: a dictionary of model field types; key is name of field and value is type of field
        :rtype: dict
        """
        types = {}
        mapper = inspect(self.db_model)

        for attr in mapper.attrs:
            name = attr.key
            column = attr.columns[0]
            python_type: Optional[type] = None

            if hasattr(column.type, "impl"):
                if hasattr(column.type.impl, "python_type"):
                    python_type = column.type.python_type
            elif hasattr(column.type, "python_type"):
                python_type = column.type.python_type
            assert python_type, f"Could not infer python_type for {column}"

            types[name] = python_type

        return types

    def __get_model_field_values(self) -> Dict[str, Any]:
        """Generate model field values for SQLAlchemy model

        :returns: a dictionary of model field values; key is name of field and value is random value
        :rtype: dict
        """
        values: Dict[str, Any] = {}

        for field, field_type in self.field_types.items():
            values[field] = self.__map_field_to_random_builder_method(field_type)()

        return values

    def __map_field_to_random_builder_method(self, field_type: Type) -> Callable:
        """Mapping between field type and RandomBuilder methods

        :returns: a RandomBuilder method for the provided type
        :rtype: func
        """
        return {
            bool: RandomBuilder.next_bool,
            date: RandomBuilder.next_date,
            datetime: RandomBuilder.next_datetime,
            float: RandomBuilder.next_float,
            int: RandomBuilder.next_int,
            str: RandomBuilder.next_str,
            time: RandomBuilder.next_time,
            timedelta: RandomBuilder.next_timedelta,
        }.get(field_type, RandomBuilder.next_str)
