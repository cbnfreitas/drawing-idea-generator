from pydantic import BaseModel as BaseSchema

from .autocomplete import autocomplete


@autocomplete
class FindRankRequestSchema(BaseSchema):
    terms: str
    url_to_find: str
    is_city: bool = True
