from pydantic import BaseModel as BaseSchema

from .autocomplete import autocomplete


@autocomplete
class MsgResponseSchema(BaseSchema):
    detail: str
