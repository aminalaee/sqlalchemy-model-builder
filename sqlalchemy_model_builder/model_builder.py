from datetime import date, datetime
from typing import Any, Dict, Optional, Type

from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy_model_builder.exceptions import ModelBuilderException
from sqlalchemy_model_builder.random_builder import RandomBuilder


class ModelBuilder:
    def __init__(self, db_model: Type, engine: Optional[Engine] = None):
        self.db_model: Type = db_model
        self.engine: Optional[Engine] = engine
        self.field_types: Dict[str, Type] = {}
        self.field_values: Dict[str, Any] = {}

    def build(self) -> Any:
        try:
            self.field_types = self.__get_model_fields()
        except NoInspectionAvailable as sqlalchemy_exception:
            raise ModelBuilderException(f"Class {self.db_model} is not a SQLAlchemy model") from sqlalchemy_exception

        self.field_values = self.__get_random_field_values()

        instance = self.db_model(**self.field_values)

        return instance

    def save(self):
        instance = self.build()

        if not self.engine:
            raise ModelBuilderException("SQLAlchemy engine not specified")

        local_session_class = sessionmaker(bind=self.engine)
        db = local_session_class()

        db.add(instance)
        db.commit()

    def __get_model_fields(self) -> Dict[str, Type]:
        types = {}
        mapper = inspect(self.db_model)

        for attr in mapper.attrs:
            if not isinstance(attr, ColumnProperty):
                continue

            if not attr.columns:
                continue

            name = attr.key
            column = attr.columns[0]
            python_type: Optional[type] = None

            if hasattr(column.type, "impl"):
                if hasattr(column.type.impl, "python_type"):
                    python_type = column.type.impl.python_type
            elif hasattr(column.type, "python_type"):
                python_type = column.type.python_type
            assert python_type, f"Could not infer python_type for {column}"

            types[name] = python_type

        return types

    def __get_random_field_values(self) -> Dict[str, Any]:
        values: Dict[str, Any] = {}

        for field, field_type in self.field_types.items():
            if field_type == bool:
                values[field] = RandomBuilder.next_bool()
            if field_type == date:
                values[field] = RandomBuilder.next_date()
            if field_type == datetime:
                values[field] = RandomBuilder.next_datetime()
            if field_type == int:
                values[field] = RandomBuilder.next_int()
            if field_type == str:
                values[field] = RandomBuilder.next_str()

        return values
