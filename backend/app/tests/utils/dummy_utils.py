
from typing import Any, Dict

from sqlalchemy.orm import Session

from ...models import DummyModel
from ...schemas.dummy_schema import DummyCreateSchema
from ...services import dummy_service
from ...tests.utils import random_lower_string


def create_random_dummy_schema() -> DummyCreateSchema:
    random_name = random_lower_string()
    return DummyCreateSchema(name=random_name)


def create_random_dummy_with_service(db: Session) -> DummyModel:
    random_dummy_schema = create_random_dummy_schema()
    return dummy_service.create(db, obj_in=random_dummy_schema)


def create_random_dummy_dict() -> Dict[str, Any]:
    return create_random_dummy_schema().dict()
