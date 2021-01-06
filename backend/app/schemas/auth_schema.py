from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel as BaseSchema
from pydantic import Field

from ..core import s
from .autocomplete import autocomplete


@autocomplete
class LoginResponseSchema(BaseSchema):
    access_token: str
    refresh_token: str


@autocomplete
class RefreshResponseSchema(BaseSchema):
    access_token: str


@autocomplete
class RefreshRequestSchema(BaseSchema):
    refresh_token: str


@autocomplete
class ActivationRequestSchema(BaseSchema):
    activation_token: str


@autocomplete
class UserPasswordBase(BaseSchema):
    new_password: str = Field(..., min_length=s.MIN_LEN_PASSWORD)

    class Config:
        extra = 'forbid'


@autocomplete
class PasswordChangeRequestSchema(UserPasswordBase):
    current_password: str = Field(..., min_length=s.MIN_LEN_PASSWORD)


@autocomplete
class PasswordResetRequestSchema(UserPasswordBase):
    reset_token: str = Field(...)
