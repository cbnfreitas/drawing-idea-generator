from sqlalchemy.orm import Session

from ...services import feature_service
from ..utils import is_schema_in_model
from ..utils.feature_utils import (create_random_feature_schema,
                                   create_random_feature_with_service)


def test_create_feature_service(db: Session) -> None:
    random_feature_schema = create_random_feature_schema()
    created_feature_model = feature_service.create(
        db, obj_in=random_feature_schema)

    assert is_schema_in_model(random_feature_schema, created_feature_model)


def test_read_one_feature_service(db: Session) -> None:
    created_feature_model = create_random_feature_with_service(db)
    created_feature_model_id = created_feature_model.id
    read_feature_model = feature_service.read(db, id=created_feature_model_id)

    assert created_feature_model == read_feature_model


def test_read_many_features_service(db: Session) -> None:
    created_feature_model = create_random_feature_with_service(db)
    read_feature_model_list = feature_service.read_many(db)

    assert created_feature_model in read_feature_model_list


def test_update_feature_service(db: Session) -> None:
    created_feature_model = create_random_feature_with_service(db)
    created_feature_model_id = created_feature_model.id
    new_random_feature_schema = create_random_feature_schema()

    updated_feature_model = feature_service.update(
        db, id=created_feature_model_id, obj_in=new_random_feature_schema)

    assert is_schema_in_model(new_random_feature_schema, updated_feature_model)


def test_delete_feature_service(db: Session) -> None:
    created_feature_model = create_random_feature_with_service(db)
    created_feature_model_id = created_feature_model.id
    assert feature_service.delete(db, id=created_feature_model_id)

    read_feature_model = feature_service.read(db, id=created_feature_model.id)
    assert not read_feature_model
