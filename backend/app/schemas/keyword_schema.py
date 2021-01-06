from datetime import date, datetime, time, timedelta
from typing import Any, List, Optional

from pydantic import BaseModel as BaseSchema

from .autocomplete import autocomplete
from .rank_schema import RankResponseNestedSchema


@autocomplete
class _KeywordCommon(BaseSchema):
    keyword: Optional[str]
    last_rank: Optional[int]
    last_rank_date: Optional[datetime]


@autocomplete
class KeywordRequestSchema(_KeywordCommon):
    domain_id: int


@autocomplete
class KeywordResponseNestedSchema(_KeywordCommon):
    id: int
    ranks: List[RankResponseNestedSchema]

    class Config:
        orm_mode = True


@autocomplete
class KeywordResponseSchema(KeywordResponseNestedSchema):
    domain_id: Optional[int]
