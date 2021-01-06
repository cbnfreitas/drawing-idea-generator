from typing import Optional, Union

from pydantic import BaseModel as BaseSchema
from pydantic import EmailStr, Field

from .autocomplete import autocomplete


@autocomplete
class UserCreateSchemaAdmin(BaseSchema):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = False
    is_admin:  Optional[bool] = False

    class Config:
        extra = 'forbid'


@autocomplete
class UserCreateSchema(BaseSchema):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    class Config:
        extra = 'forbid'


user_create_schemas = Union[UserCreateSchemaAdmin, UserCreateSchema]


@autocomplete
class UserUpdateSchema(BaseSchema):
    password:  Optional[str] = None
    full_name: Optional[str] = None

    class Config:
        extra = 'forbid'


@autocomplete
class UserUpdateActivateSchema(BaseSchema):
    is_active = True

    class Config:
        extra = 'forbid'


@autocomplete
class UserReadSchema(BaseSchema):
    id: int
    full_name: Optional[str]
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
