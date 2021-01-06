from typing import Tuple

from pydantic import EmailStr
from sqlalchemy.orm import Session

from ...models.user_model import UserModel
from ...schemas.user_schema import UserCreateSchema, UserUpdateSchema
from ...services.user_service import user_service
from ..utils import random_email, random_lower_string


def create_or_update_user_via_service(
        db: Session, email: str = None, password: str = None
) -> UserModel:
    '''
    Create or update a user with a given email.
    Email is randomly generated if not provided.
    Password is set if provided, otherwise it is randomly generated for creation.
    '''

    if not email:
        email = random_email()

    user_db = user_service.read_by_email(db, email=email)
    if not user_db:
        if not password:
            password = random_lower_string()
        user_in = UserCreateSchema(email=EmailStr(email), password=password)
        user_db = user_service.create(db=db, obj_in=user_in)
    elif password:
        user_db = user_service.update(
            db, id=user_db.id, obj_in=UserUpdateSchema(password=password))

    return user_db
