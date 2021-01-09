
from typing import Any, Dict

from pydantic import BaseModel as BaseSchema
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from ...core.session import engine
from ...models import BaseModel
from ...services.base_service import BaseService
from ...tests.utils import random_lower_string


class DummyModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


table_objects = [DummyModel.__table__]  # type: ignore
BaseModel.metadata.create_all(engine, tables=table_objects)  # type: ignore


class DummyCreateSchema(BaseSchema):
    name: str


class DummyReadSchema(BaseSchema):
    id: int
    name: str

    class Config:
        orm_mode = True


dummy_service = BaseService[DummyModel,
                            DummyCreateSchema, DummyCreateSchema](DummyModel, DummyModel.id)


def create_random_dummy_schema() -> DummyCreateSchema:
    random_name = random_lower_string()
    return DummyCreateSchema(name=random_name)


def create_random_dummy_with_service(db: Session) -> DummyModel:
    random_dummy_schema = create_random_dummy_schema()
    return dummy_service.create(db, obj_in=random_dummy_schema)


def create_random_dummy_dict() -> Dict[str, Any]:
    return create_random_dummy_schema().dict()
