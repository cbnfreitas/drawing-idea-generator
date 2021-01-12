from http import HTTPStatus
from typing import Any, List

import app.core.depends as depends
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column
from sqlalchemy.orm import Session

from ..core import route_paths
from ..models.user_model import UserModel
from ..schemas.user_schema import (UserCreateSchema, UserReadSchema,
                                   UserUpdateSchema)
from ..services import user_service

user_route = APIRouter()


@user_route.get(route_paths.ROUTE_USER, response_model=List[UserReadSchema])
def read_users(
        db: Session = Depends(depends.get_db),
        _current_admin: UserModel = Depends(
            depends.get_admin_from_access_token),
        *,
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Retrieve many users, including pagination
    """
    users = user_service.read_many(db, skip=skip, limit=limit)
    return users


@user_route.post(route_paths.ROUTE_USER, response_model=UserReadSchema)
def create_user(
        db: Session = Depends(depends.get_db),
        _current_admin: UserModel = Depends(
            depends.get_admin_from_access_token),
        *,
        user_in: UserCreateSchema
) -> Any:
    """
    Create new user.
    """
    user_with_in_email = user_service.read_by_email(db, email=user_in.email)
    if user_with_in_email:
        raise HTTPException(
            status_code=400,
            detail="A user with this e-mail already exists in the system.",
        )
    user = user_service.create(db, obj_in=user_in)
    return user


def update_user_by_helper(
        db: Session = Depends(depends.get_db),
        *,
        user_id: int,
        user_in: UserUpdateSchema
) -> UserModel:
    """
    Update a user by id. This is used by both user_me and user/id
    """
    user = user_service.read(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="User_id not found",
        )

    user = user_service.update(db, id=user.id, obj_in=user_in)
    return user


@user_route.get(f"{route_paths.ROUTE_USER}/{{user_id}}", response_model=UserReadSchema)
def read_user_by_id(
        db: Session = Depends(depends.get_db),
        _current_admin: UserModel = Depends(
            depends.get_admin_from_access_token),
        *,
        user_id: int
) -> Any:
    """
    Get a specific user by user_id.
    """
    return user_service.read(db, id=user_id)


@user_route.put(f"{route_paths.ROUTE_USER}/{{user_id}}", response_model=UserReadSchema)
def update_user_by_id(
        db: Session = Depends(depends.get_db),
        _current_admin: UserModel = Depends(
            depends.get_admin_from_access_token),
        *,
        user_id: int,
        user_in: UserUpdateSchema
) -> Any:
    """
    Update a user.
    """
    user = update_user_by_helper(db, user_id=user_id, user_in=user_in)
    return user


@user_route.delete(f"{route_paths.ROUTE_USER}/{{user_id}}")
def remove_user_by_id(
        db: Session = Depends(depends.get_db),
        _current_user: UserModel = Depends(
            depends.get_admin_from_access_token),
        *,
        user_id: int
) -> Any:
    """
    Remove a user.
    """
    deleted_user = user_service.delete(db, id=user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this user_id does not exist in the system.",
        )
    return
