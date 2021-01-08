
from typing import Any, Dict

from sqlalchemy.orm import Session

from ...models.features_model import FeatureModel
from ...schemas.feature_schema import FeatureCreateSchema
from ...services import feature_service
from ...tests.utils import random_integer, random_lower_string


def create_random_feature_schema() -> FeatureCreateSchema:
    random_name = random_lower_string()
    return FeatureCreateSchema(name=random_name)


def create_random_feature_with_service(db: Session) -> FeatureModel:
    random_feature_schema = create_random_feature_schema()
    return feature_service.create(db, obj_in=random_feature_schema)


# def create_random_rank_dict(random_rank: int = None, random_keyword_id: int = None) -> Dict[str, Any]:
#     return create_random_rank_schema(random_rank, random_keyword_id).dict()


# def assert_schema_db_rank(schema: RankRequestSchema, model: RankModel):
#     assert schema.rank == model.rank
#     assert schema.keyword_id == model.keyword_id
