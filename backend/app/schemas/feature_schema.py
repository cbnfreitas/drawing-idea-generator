from typing import Any, List, Optional

from pydantic import BaseModel as BaseSchema

from ..models import FeatureModel
from .autocomplete import autocomplete
from .value_schema import ValueReadSchema

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic


@autocomplete
class FeatureCreateSchema(BaseSchema):
    name: str


@autocomplete
class FeatureReadSchema(BaseSchema):
    id: int
    name: str
    values: List[ValueReadSchema]

    class Config:
        orm_mode = True
