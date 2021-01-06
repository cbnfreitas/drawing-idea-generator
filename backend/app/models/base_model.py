from typing import Any

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class BaseModel:
    __name__: str

    # Generate __tablename__ automatically,
    # remove the suffix 'model' if necessary
    @declared_attr
    def __tablename__(self) -> str:
        table_name = self.__name__.lower()
        if table_name[-5:] == 'model':
            table_name = table_name[:-5]
        return table_name
