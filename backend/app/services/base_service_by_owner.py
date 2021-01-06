from datetime import date, datetime
from http import HTTPStatus
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as BaseSchema
from sqlalchemy import Column, and_
from sqlalchemy.orm import Session

from ..models.base_model import BaseModel
from .base_service import (BaseModelType, BaseService, CreateSchemaType,
                           UpdateSchemaType)


class BaseServiceByOwner(BaseService[BaseModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Database CRUD with Pydantic as input. It utilizes model_id as matching criterion.

    **Parameters**
    * `BaseModelType`: A SQLAlchemy BaseModel
    * `CreateSchemaType`: A Pydantic BaseSchema
    * `UpdateSchemaType`: A Pydantic BaseSchema
    """

    def __init__(
            self,
            model: Type[BaseModelType],
            model_id: Column,
            model_owner_id: Column
    ):
        self.model = model
        self.model_id = model_id
        self.model_owner_id = model_owner_id

    def create_by_owner(
            self,
            db: Session,
            *,
            obj_in: CreateSchemaType,
            owner_id: int
    ) -> BaseModelType:
        """
        Save `obj_in` as a new `ModelType` in the database and
        return the corresponding `ModelType`.
        """
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data[self.model_owner_id.name] = owner_id
        return self._create(db, obj_in=obj_in_data)

    def read_by_owner(
            self,
            db: Session,
            id: int,
            owner_id: int
    ) -> BaseModelType:
        """
        Return a `ModelType` by `id` from the database.
        """
        return self._read(db, and_(self.model_id == id,
                                   self.model_owner_id == owner_id)).first()

    def read_many_by_owner(
            self,
            db: Session,
            owner_id: int,
            *,
            skip: int = None,
            limit: int = None
    ) -> List[BaseModelType]:
        """
        Return a list of `ModelType`s from the database, including pagination.
        """
        return self._read(db, self.model_owner_id == owner_id).offset(skip).limit(limit).all()

    def update_by_owner(
            self,
            db: Session,
            *,
            id: int,
            owner_id: int,
            obj_in: UpdateSchemaType
    ) -> BaseModelType:
        """
        Update `db_obj` with `obj_in` in the database and
        return the corresponding `ModelType`.
        """
        return self._update(db, and_(self.model_id == id, self.model_owner_id == owner_id), update_data=obj_in.dict(exclude_unset=True)).first()

    def delete_by_owner(
            self,
            db: Session,
            id: int,
            owner_id: int
    ):
        """
        Delete a `ModelType` by `id` in the database and
        return the deleted `ModelType`.
        """
        self._delete(db, and_(self.model_id == id,
                              self.model_owner_id == owner_id))
