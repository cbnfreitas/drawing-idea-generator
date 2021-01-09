from datetime import datetime
from typing import Any, Dict

import app.core.error_msgs as error_msgs
import app.core.security as security
from fastapi import Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.engine import strategies
from sqlalchemy.orm import Session

from ..core import route_paths
from ..core.session import SessionLocal
from ..models import UserModel
from ..schemas.auth_schema import ActivationRequestSchema, RefreshRequestSchema
from ..services import user_service

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=route_paths.ROUTE_AUTH_LOGIN
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_from_access_token(
        db: Session = Depends(get_db),
        access_token: str = Depends(reusable_oauth2)
) -> Dict[str, Any]:

    try:
        user_token_data = security.decode_sub_jwt(db, access_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0])

    return user_token_data


def get_admin_from_access_token(
        admin_token_data: Dict[str, Any] = Depends(get_user_from_access_token),
) -> Dict[str, Any]:

    if not admin_token_data["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_msgs.ONLY_AVAILABLE_TO_ADMIN)

    return admin_token_data


def get_user_db_from_token(
        token: str,
        token_type: str,
        db: Session = Depends(get_db)
) -> UserModel:

    try:
        token_data = security.decode_sub_jwt(db, token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.args[0])

    if token_type == 'refresh':
        user_db = user_service.read(
            db, id=token_data["user_id"])
    else:
        if "is_active" not in token_data or not token_data["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msgs.INVALID_TOKEN)
        user_db = user_service.read_by_email(
            db, email=token_data["email"])

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msgs.USER_NOT_FOUND)

    token_timestamp = token_data["token_timestamp"]
    auth_change_timestamp = user_db.last_auth_change.timestamp()

    if token_timestamp < auth_change_timestamp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msgs.STALE_CREDENTIALS)

    return user_db


def get_user_db_from_refresh_token(
        refresh_body: RefreshRequestSchema,
        db: Session = Depends(get_db)
) -> UserModel:
    return get_user_db_from_token(refresh_body.refresh_token, "refresh", db)


def get_user_db_from_activation_token(
        activation_body: ActivationRequestSchema,
        db: Session = Depends(get_db)
) -> UserModel:
    return get_user_db_from_token(activation_body.activation_token, "activation", db)
