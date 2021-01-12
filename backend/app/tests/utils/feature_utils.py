
from typing import Any, Dict

from sqlalchemy.orm import Session

from ...models import FeatureModel
from ...schemas.feature_schema import FeatureCreateSchema
from ...services import feature_service
from ...tests.utils import random_integer, random_lower_string


def create_random_feature_schema(db: Session) -> FeatureCreateSchema:
    random_name = random_lower_string()
    return FeatureCreateSchema(name=random_name)


def create_random_feature_with_service(db: Session) -> FeatureModel:
    random_feature_schema = create_random_feature_schema(db)
    return feature_service.create(db, obj_in=random_feature_schema)


def create_random_feature_dict(db: Session) -> Dict[str, Any]:
    return create_random_feature_schema(db).dict()
