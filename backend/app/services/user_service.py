
from datetime import datetime
from typing import Any, Dict, Optional, Type, Union

import app.core.security as security
from app.core.utils import schema_or_dict_to_dict
from sqlalchemy import Column
from sqlalchemy.orm import Session

from ..models.user_model import UserModel
from ..schemas.user_schema import UserUpdateSchema, user_create_schemas
from .base_service import BaseService


class BaseUserService(BaseService[UserModel, user_create_schemas, UserUpdateSchema]):
    """
    User and authentication
    """

    def read_by_email(
            self,
            db: Session,
            *,
            email: str
    ) -> UserModel:
        """
        Return a `UserModel` by `email` from the database.
        """
        return self._read(db, self.model.email == email).first()

    def create(
            self,
            db: Session,
            *,
            obj_in: user_create_schemas
    ) -> UserModel:
        """
        Save `obj_in` as a new `UserModel` in the database,
        with obj_in.password replaced by a hashed password, and
        return the corresponding `UserModel`.
        """
        obj_data = obj_in.dict()
        obj_data['hashed_password'] = security.get_password_hash(
            obj_in.password)
        del obj_data["password"]

        return self._create(db, obj_in=obj_data)

    def update(
            self,
            db: Session,
            *,
            id: int,
            obj_in:  Union[UserUpdateSchema, Dict[Column, Any]]
    ) -> UserModel:
        """
        Update `db_obj` by `obj_in` in the database.
        If a new `password` is provided, replaced it by a
        `hashed_password` and update `password_last_change_date`.
        Return the corresponding `UserModel`.
        """
        update_data = schema_or_dict_to_dict(obj_in)

        auth_change = False
        if update_data.get("password"):
            hashed_password = security.get_password_hash(
                update_data["password"])

            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            auth_change = True

        if update_data.get("is_active") or update_data.get("is_admin"):
            auth_change = True

        if auth_change:
            update_data["last_auth_change"] = datetime.utcnow()

        return self._update(db, conditions=self.model.id == id, update_data=update_data).first()

    def authenticate(
            self,
            db: Session,
            *,
            email: str = None,
            user_id: int = None,
            password: str
    ) -> Optional[UserModel]:
        """
        Return the `UserModel` matching `email` and (hashed) `password`.
        """
        if user_id:
            user = self.read(db, id=user_id)
        elif email:
            user = self.read_by_email(db, email=email)
        else:
            return None

        if not user or not security.verify_password(password, user.hashed_password):
            return None

        return user


user_service = BaseUserService(UserModel, UserModel.id)
