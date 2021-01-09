#
# This files contains all routes related with authorization
#
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Dict

import app.core.depends as depends
import app.core.error_msgs as error_msgs
import app.core.security as security
import app.core.sucess_msgs as sucess_msgs
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core import route_paths
from ..core.email_builder import (send_activation_email,
                                  send_reset_password_email)
from ..core.security import (create_activation_token,
                             create_password_reset_token, decode_sub_jwt)
from ..models.user_model import UserModel
from ..schemas.auth_schema import (LoginResponseSchema,
                                   PasswordChangeRequestSchema,
                                   PasswordResetRequestSchema,
                                   RefreshResponseSchema)
from ..schemas.msg_schema import MsgResponseSchema
from ..schemas.user_schema import UserCreateSchema, UserUpdateSchema
from ..services import denied_token_redis, user_service

auth_router = APIRouter()


@auth_router.post(route_paths.ROUTE_AUTH_REGISTER_AND_ACTIVATION_TOKEN_TO_EMAIL, response_model=MsgResponseSchema)
def registration(
        db: Session = Depends(depends.get_db),
        *,
        new_user_in: UserCreateSchema
) -> Any:
    """
    Register a new normal user as inactive and send activation token to his/her e-mail.
    """
    user_with_this_email = user_service.read_by_email(
        db, email=new_user_in.email)

    if user_with_this_email:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=error_msgs.EMAIL_ALREADY_IN_USE)

    new_user = user_service.create(db, obj_in=new_user_in)
    activation_token = create_activation_token(email=new_user.email)
    send_activation_email(user=new_user, token=activation_token)

    return MsgResponseSchema(detail=sucess_msgs.ACTIVATION_SENT_TO_EMAIL)


@auth_router.post(route_paths.ROUTE_AUTH_ACTIVATION, response_model=MsgResponseSchema)
def activation(
        user_db: UserModel = Depends(
            depends.get_user_db_from_activation_token),
        db: Session = Depends(depends.get_db),
) -> Any:
    """
    After receiving an activation token from e-mail, activates the user.
    """

    user_service.update(db, id=user_db.id,
                        obj_in={UserModel.is_active: True})
    return MsgResponseSchema(detail=sucess_msgs.USER_ACTIVATED_SUCCESSFULLY)


@auth_router.post(route_paths.ROUTE_AUTH_LOGIN, response_model=LoginResponseSchema)
def login(
        db: Session = Depends(depends.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login.
    Return an access token if the correct `username` (e-mail) and `password` are provided.
    """

    user = user_service.authenticate(
        db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=error_msgs.INCORRECT_EMAIL_OR_PASSWORD)

    access_token = security.create_access_token(
        user_id=user.id, is_admin=user.is_admin)
    refresh_token = security.create_refresh_token(user_id=user.id)

    return LoginResponseSchema(access_token=access_token, refresh_token=refresh_token)


@auth_router.post(route_paths.ROUTE_AUTH_LOGOUT, response_model=MsgResponseSchema)
def logout(
        db: Session = Depends(depends.get_db),
        user_token_data: Dict[str, Any] = Depends(
            depends.get_user_from_access_token),
        token: str = Depends(depends.reusable_oauth2)
) -> Any:
    """
    Add current token to deny list, so it's no longer valid.
    """
    denied_token_redis.set(token, "")

    return MsgResponseSchema(detail=sucess_msgs.LOGOUT_SUCCESSFULLY)


@auth_router.post(route_paths.ROUTE_AUTH_REFRESH, response_model=RefreshResponseSchema)
def refresh(
        user_db_refresh: UserModel = Depends(
            depends.get_user_db_from_refresh_token)
) -> Any:
    """
    Provides a new access_token for a valid refresh_token
    """

    new_access_token = security.create_access_token(
        user_id=user_db_refresh.id, is_admin=user_db_refresh.is_admin)

    return RefreshResponseSchema(access_token=new_access_token)


@auth_router.post(route_paths.ROUTE_AUTH_PASSWORD_CHANGE, response_model=MsgResponseSchema)
def password_change(
        payload: PasswordChangeRequestSchema,
        db: Session = Depends(depends.get_db),
        current_user_token_data: Dict[str, Any] = Depends(
            depends.get_user_from_access_token)
) -> Any:
    """
    Allows a logged user to change password.
    """
    user = user_service.authenticate(
        db, user_id=current_user_token_data['user_id'], password=payload.current_password)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=error_msgs.INVALID_CURRENT_PASSWORD)

    user_service.update(db, id=user.id, obj_in=UserUpdateSchema(
        password=payload.new_password))
    return MsgResponseSchema(detail=sucess_msgs.PASSWORD_UPDATED_SUCCESSFULLY)


@auth_router.post(f"{route_paths.ROUTE_AUTH_PASSWORD_RESET_TOKEN_TO_EMAIL}/{{email}}",
                  response_model=MsgResponseSchema)
def password_reset_token_to_email(
        email: str, db: Session = Depends(depends.get_db)
) -> Any:
    """
    Password Recovery.
    """
    user = user_service.read_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error_msgs.UNREGISTERED_EMAIL)

    password_reset_token = create_password_reset_token(email=email)
    send_reset_password_email(user=user, token=password_reset_token)

    return MsgResponseSchema(detail=sucess_msgs.PASSWORD_RECOVERY_SENT_TO_EMAIL)


@auth_router.post(route_paths.ROUTE_AUTH_PASSWORD_RESET, response_model=MsgResponseSchema)
def password_reset(
        payload: PasswordResetRequestSchema,
        db: Session = Depends(depends.get_db),
) -> Any:
    """
    After receiving a token from e-mail, it allows the user to define a new password.
    """
    try:
        reset_token_data = decode_sub_jwt(db, token=payload.reset_token)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=e.args[0])

    user = user_service.read_by_email(db, email=reset_token_data["email"])
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error_msgs.EMAIL_DOES_NOT_EXIST)

    user_service.update(db, id=user.id, obj_in=UserUpdateSchema(
        password=payload.new_password))
    return MsgResponseSchema(detail=sucess_msgs.PASSWORD_UPDATED_SUCCESSFULLY)
