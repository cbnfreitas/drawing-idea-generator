from typing import Any, List, Optional

from pydantic import BaseModel as BaseSchema

from ..models import FeaturesModel
from .autocomplete import autocomplete

# from pydantic_sqlalchemy import sqlalchemy_to_pydantic


@autocomplete
class FeatureCreateSchema(BaseSchema):
    name: str


@autocomplete
class FeatureReadSchema(BaseSchema):
    id: int
    name: str
