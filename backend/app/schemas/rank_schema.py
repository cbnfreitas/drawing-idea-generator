from typing import Any, Optional

from pydantic import BaseModel as BaseSchema

from .autocomplete import autocomplete


@autocomplete
class _RankCommon(BaseSchema):
    rank: Optional[int]


@autocomplete
class RankRequestSchema(_RankCommon):
    keyword_id: int


@autocomplete
class RankResponseNestedSchema(_RankCommon):
    id: int
    date_time: Any

    class Config:
        orm_mode = True


@autocomplete
class RankResponseSchema(RankResponseNestedSchema):
    keyword_id: Optional[int]
