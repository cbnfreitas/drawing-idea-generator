import pytest
from sqlalchemy.orm import Session

from ...services import feature_service
from ..utils import is_schema_in_model
from ..utils.dummy_utils import (_dummy_service, create_random_dummy_schema,
                                 create_random_dummy_with_service,
                                 dummy_service)
from ..utils.feature_utils import create_random_feature_schema


@pytest.mark.parametrize("entity_service, create_random_entity_schema",
                         [
                             (dummy_service, create_random_dummy_schema),
                             (feature_service, create_random_feature_schema)
                         ])
class TestBaseService:
    def test_create_dummy_service(self, db: Session, entity_service, create_random_entity_schema) -> None:
        random_entity_schema = create_random_entity_schema()
        created_entity_model = entity_service.create(
            db, obj_in=random_entity_schema)
        assert is_schema_in_model(random_entity_schema, created_entity_model)


# def test_read_one_dummy_service(db: Session) -> None:
#     created_dummy_model = create_random_dummy_with_service(db)
#     created_dummy_model_id = created_dummy_model.id
#     read_dummy_model = dummy_service.read(db, id=created_dummy_model_id)

#     assert created_dummy_model == read_dummy_model


# def test_read_many_dummies_service(db: Session) -> None:
#     created_dummy_model = create_random_dummy_with_service(db)
#     read_dummy_model_list = dummy_service.read_many(db)

#     assert created_dummy_model in read_dummy_model_list


# def test_update_dummy_service(db: Session) -> None:
#     created_dummy_model = create_random_dummy_with_service(db)
#     created_dummy_model_id = created_dummy_model.id
#     new_random_dummy_schema = create_random_dummy_schema()

#     updated_dummy_model = dummy_service.update(
#         db, id=created_dummy_model_id, obj_in=new_random_dummy_schema)

#     assert is_schema_in_model(new_random_dummy_schema, updated_dummy_model)


# def test_delete_dummy_service(db: Session) -> None:
#     created_dummy_model = create_random_dummy_with_service(db)
#     created_dummy_model_id = created_dummy_model.id
#     assert dummy_service.delete(db, id=created_dummy_model_id)

#     read_dummy_model = dummy_service.read(db, id=created_dummy_model.id)
#     assert not read_dummy_model


# def test_fail_to_delete_dummy_service_with_non_existing_id(db: Session) -> None:
#     wrong_dummy_model_id = -1
#     assert not dummy_service.delete(db, id=wrong_dummy_model_id)


# def test_init_private_service(db: Session) -> None:
#     assert _dummy_service
