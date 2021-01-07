from typing import Any, List, Optional

from pydantic import BaseModel as BaseSchema
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from ..models import FeaturesModel
from .autocomplete import autocomplete


@autocomplete
class FeatureCreateSchema(BaseSchema):
    name: str


@autocomplete
class FeatureReadSchema(BaseSchema):
    id: int
    name: str
