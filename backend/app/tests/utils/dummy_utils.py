
from typing import Any, Dict, Optional

from pydantic import BaseModel as BaseSchema
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from ...core.session import engine
from ...models import BaseModel
from ...schemas.autocomplete import autocomplete
from ...services.base_service import BaseService, _BaseService
from ...tests.utils import random_lower_string


class DummyModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    stars = Column(Integer, index=True)


table_objects = [DummyModel.__table__]  # type: ignore
BaseModel.metadata.create_all(engine, tables=table_objects)  # type: ignore


@autocomplete
class DummyCreateSchema(BaseSchema):
    name: str
    stars: Optional[int] = None


@autocomplete
class DummyUpdateSchema(BaseSchema):
    name:  Optional[str] = None
    stars: Optional[int] = None


@autocomplete
class DummyReadSchema(BaseSchema):
    id: int
    name: str
    stars: Optional[int] = None

    class Config:
        orm_mode = True


_dummy_service = _BaseService[DummyModel](DummyModel)

dummy_service = BaseService[DummyModel,
                            DummyCreateSchema, DummyUpdateSchema](DummyModel, DummyModel.id)


def create_random_dummy_schema(db: Session) -> DummyCreateSchema:
    random_name = random_lower_string()
    return DummyCreateSchema(name=random_name)


def create_random_dummy_with_service(db: Session) -> DummyModel:
    random_dummy_schema = create_random_dummy_schema(db)
    return dummy_service.create(db, obj_in=random_dummy_schema)


def create_random_dummy_dict(db: Session) -> Dict[str, Any]:
    return create_random_dummy_schema(db).dict()
