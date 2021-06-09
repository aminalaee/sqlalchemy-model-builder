from datetime import date, datetime, time, timedelta
from typing import Any, Callable, Dict, Optional, Type

from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.session import Session

from sqlalchemy_model_builder.exceptions import ModelBuilderException
from sqlalchemy_model_builder.random_builder import RandomBuilder


class ModelBuilder:
    def __init__(self, db_model: Type, minimal: bool = False):
        self.db_model: Type = db_model
        self.field_values: Dict[str, Any] = {}
        self.minimal: bool = minimal

    def build(self) -> Any:
        """Build SQLAlchemy model with random data and return it without persisting into database

        :returns: a SQLAlchemy database model with generated random data
        :rtype: Any
        """
        try:
            self.field_values = self.__get_model_fields()
        except NoInspectionAvailable as sqlalchemy_exception:
            raise ModelBuilderException(f"Class {self.db_model} is not a SQLAlchemy model") from sqlalchemy_exception

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
        """Get model field and values from SQLAlchemy model

        :returns: a dictionary of model field values; key is name of field and value is random value
        :rtype: dict
        """
        values = {}
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

            if self.minimal and column.nullable:
                continue

            values[name] = self.__map_field_to_random_builder_method(python_type)()

        return values

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
