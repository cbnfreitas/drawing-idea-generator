
from typing import Any, Dict

from app.tests.utils.feature_utils import create_random_feature_with_service
from sqlalchemy.orm import Session

from ...models import ValueModel
from ...schemas.value_schema import ValueCreateSchema
from ...services import value_service
from ...tests.utils import random_integer, random_lower_string


def create_random_value_schema(db: Session) -> ValueCreateSchema:
    random_value = random_lower_string()
    random_feature = create_random_feature_with_service(db)
    random_feature_id = random_feature.id
    return ValueCreateSchema(value=random_value, feature_id=random_feature_id)


def create_random_value_with_service(db: Session) -> ValueModel:
    random_value_schema = create_random_value_schema(db)
    return value_service.create(db, obj_in=random_value_schema)


def create_random_value_dict(db: Session) -> Dict[str, Any]:
    return create_random_value_schema(db).dict()
