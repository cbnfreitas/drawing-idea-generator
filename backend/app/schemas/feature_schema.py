from typing import Any, List, Optional

from pydantic import BaseModel as BaseSchema

from ..models import FeatureModel
from .autocomplete import autocomplete

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic


@autocomplete
class FeatureCreateSchema(BaseSchema):
    value: str
    feature_id: int


@autocomplete
class FeatureReadSchema(BaseSchema):
    id: int
    value: str
    feature_id: int

    class Config:
        orm_mode = True
