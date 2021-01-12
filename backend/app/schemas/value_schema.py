from typing import Any, List, Optional

from pydantic import BaseModel as BaseSchema

from .autocomplete import autocomplete


@autocomplete
class ValueCreateSchema(BaseSchema):
    value: str
    feature_id: int


@autocomplete
class ValueReadSchema(BaseSchema):
    id: int
    value: str
    feature_id: int

    class Config:
        orm_mode = True

class ValueReadSchemaNested(BaseSchema):
    id: int
    value: str

    class Config:
        orm_mode = True
