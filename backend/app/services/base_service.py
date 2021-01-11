from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from app.core.utils import schema_or_dict_to_dict
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as BaseSchema
from sqlalchemy import Column
from sqlalchemy.orm import Session

from ..models.base_model import BaseModel

BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)


class _BaseService(Generic[BaseModelType]):
    """
    Database CRUD with Dict as input. It utilizes `conditions` for filtering.

    **Parameters**
    * `BaseModelType`: A SQLAlchemy BaseModel
    """

    def __init__(
            self,
            model: Type[BaseModelType]
    ):
        self.model = model

    def _create(
            self,
            db: Session,
            *,
            obj_in: Dict[str, Any],
    ) -> BaseModelType:
        """
        Save `obj_in` as a new `ModelType` in the database and
        return the corresponding `ModelType`.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # try:
        #     db.commit()
        #     db.refresh(db_obj)
        # except Exception as e:
        #     db.rollback()
        #     raise e
        return db_obj

    def _read(
            self,
            db: Session,
            conditions=True
    ) -> Any:
        """
        Return a `ModelType` matching `conditions` from the database.
        """
        return db.query(self.model).filter(conditions)

    def _update(
            self,
            db: Session,
            conditions=False,
            *,
            update_data: Dict[str, Any]
    ) -> Any:
        """
        Update `db_obj` with `update_data` based on `conditions` in the database and
        """
        db_obj = db.query(self.model).filter(conditions)
        db_obj.update(update_data)
        db.commit()

        # try:
        #     db.commit()
        # except Exception as e:
        #     db.rollback()
        #     raise e

        return db_obj

    def _delete(
            self,
            db: Session,
            conditions=True
    ) -> bool:
        """
        Delete a `ModelType` by `id` on the database.
        """
        db_obj = db.query(self.model).filter(conditions)
        if db_obj.count() == 0:
            return False

        db_obj.delete()
        db.commit()

        # try:
        #     db.commit()
        # except Exception as e:
        #     db.rollback()
        #     raise e

        return True


class BaseService(_BaseService, Generic[BaseModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Database CRUD with Pydantic as input. It utilizes the column model_id as matching criterion.

    **Parameters**
    * `BaseModelType`: A SQLAlchemy BaseModel
    * `CreateSchemaType`: A Pydantic BaseSchema
    * `UpdateSchemaType`: A Pydantic BaseSchema
    """

    def __init__(
            self,
            model: Type[BaseModelType],
            model_id: Column
    ):
        self.model = model
        self.model_id = model_id

    def create(
            self,
            db: Session,
            *,
            obj_in: CreateSchemaType,
    ) -> BaseModelType:
        """
        Save `obj_in` as a new `ModelType` in the database and
        return the corresponding `ModelType`.
        """
        return self._create(db, obj_in=jsonable_encoder(obj_in))

    def read(
            self,
            db: Session,
            id: int
    ) -> BaseModelType:
        """
        Return a `ModelType` by `id` from the database.
        """
        return self._read(db, self.model_id == id).first()

    def read_many(
            self,
            db: Session,
            *,
            skip: int = None,
            limit: int = None
    ) -> List[BaseModelType]:
        """
        Return a list of `ModelType`s from the database, including pagination if necessary.
        """
        return self._read(db).offset(skip).limit(limit).all()

    def update(
            self,
            db: Session,
            *,
            id: int,
            obj_in: Union[UpdateSchemaType, Dict[Column, Any]]
    ) -> BaseModelType:
        """
        Update `db_obj` with `obj_in` in the database and
        return the corresponding `ModelType`.
        """
        obj_in_data = schema_or_dict_to_dict(obj_in)
        return self._update(db, conditions=self.model_id == id, update_data=obj_in_data).first()

    def delete(
            self,
            db: Session,
            id: int
    ) -> bool:
        """
        Delete a `ModelType` by `id` in the database and
        return the deleted `ModelType`.
        """
        return self._delete(db, self.model_id == id)
