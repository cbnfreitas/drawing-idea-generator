from typing import Any

from sqlalchemy.orm import Session

from ...schemas.feature_schema import FeatureCreateSchema
from ...services import feature_service
from ..utils import random_integer, random_lower_string


def test_create_feature_service(db: Session) -> None:
    random_feature_data = random_lower_string()
    random_feature = FeatureCreateSchema(random_feature_data)
    created_rank_db = feature_service.create(db, obj_in=random_feature)
    assert created_rank_db == random_feature_data


# def test_read_rank_service(db: Session) -> None:
#     created_rank_db = create_random_rank_with_service(db)
#     read_rank_db = rank_service.read(db, id=created_rank_db.id)
#     assert created_rank_db == read_rank_db


# def test_read_many_rank_service(db: Session) -> None:
#     created_rank_db = create_random_rank_with_service(db)
#     read_list_rank_db = rank_service.read_many(db)
#     assert created_rank_db in read_list_rank_db


# def test_update_rank_service(db: Session) -> None:
#     created_rank_db = create_random_rank_with_service(db)
#     new_random_rank_schema = create_random_rank_schema()
#     updated_rank_db = rank_service.update(
#         db, id=created_rank_db.id, obj_in=new_random_rank_schema)

#     assert_schema_db_rank(new_random_rank_schema, updated_rank_db)


# def test_delete_rank_service(db: Session) -> None:
#     created_rank_db = create_random_rank_with_service(db)
#     rank_service.delete(db, id=created_rank_db.id)
