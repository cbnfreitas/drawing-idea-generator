from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ...core.security import verify_password
from ...schemas.user_schema import UserCreateSchemaAdmin, UserUpdateSchema
from ...services import user_service
from ..utils import random_email, random_lower_string


def test_create_user_service(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateSchemaAdmin(
        email=EmailStr(email), password=password, is_active=True)
    before_creation_time_stamp = datetime.utcnow().timestamp()
    user = user_service.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")
    assert before_creation_time_stamp <= user.last_auth_change.timestamp()


def test_authenticate(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateSchemaAdmin(
        email=EmailStr(email), password=password, is_active=True)
    user = user_service.create(db, obj_in=user_in)
    authenticated_user = user_service.authenticate(
        db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_fail_to_authenticate_wrong_password(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateSchemaAdmin(
        email=EmailStr(email), password=password, is_active=True)
    _user = user_service.create(db, obj_in=user_in)
    wrong_password = random_lower_string()
    none_user = user_service.authenticate(
        db, email=email, password=wrong_password)
    assert none_user is None


def test_fail_to_authenticate_email_not_found(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    none_user = user_service.authenticate(
        db, email=email, password=password)
    assert none_user is None


def test_fail_to_authenticate_missing_user_id_and_email(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    none_user = user_service.authenticate(db, password=password)
    assert none_user is None


def test_read_user_by_email(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreateSchemaAdmin(
        email=EmailStr(email), password=password, is_admin=True,  is_active=True)
    user_created = user_service.create(db, obj_in=user_in)
    user_read = user_service.read_by_email(db, email=user_created.email)
    assert user_read
    assert jsonable_encoder(user_created) == jsonable_encoder(user_read)


def update_user_password_and_assert(db: Session, obj_in: Any) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreateSchemaAdmin(
        email=EmailStr(email), password=password, is_admin=True, is_active=True)
    user = user_service.create(db, obj_in=user_in)

    new_password = obj_in['password'] if isinstance(
        obj_in, dict) else obj_in.password

    before_update_time_stamp = datetime.utcnow().timestamp()
    user_db = user_service.update(
        db, id=user.id, obj_in=obj_in)  # type: ignore
    assert user_db
    assert before_update_time_stamp <= user_db.last_auth_change.timestamp()
    assert user.email == user_db.email
    assert verify_password(new_password, user_db.hashed_password)


def test_update_user_as_schema(db: Session) -> None:
    new_password = random_lower_string()
    user_in_update_schema = UserUpdateSchema(password=new_password)
    update_user_password_and_assert(db, obj_in=user_in_update_schema)
