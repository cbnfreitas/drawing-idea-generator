from typing import Any, List, Optional

from pydantic import BaseModel as BaseSchema

from .autocomplete import autocomplete
from .keyword_schema import KeywordResponseNestedSchema


@autocomplete
class _DomainCommon(BaseSchema):
    url: str


@autocomplete
class DomainRequestSchema(_DomainCommon):
    class Config:
        extra = 'forbid'


@autocomplete
class DomainResponseSchema(_DomainCommon):
    id: int
    keywords: List[KeywordResponseNestedSchema]

    class Config:
        orm_mode = True
