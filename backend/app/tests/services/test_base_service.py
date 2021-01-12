import pytest
from sqlalchemy.orm import Session

from ...routes.base_route import base_route
from ...services.base_service import BaseService
from ..utils import is_schema_in_model, see_also


class _TestBaseService:
    def test_create_entity_service(
            self, db: Session, entity_service: BaseService, create_random_entity_schema, create_random_entity_with_service
    ) -> None:
        random_entity_schema = create_random_entity_schema(db)
        created_entity_model = entity_service.create(
            db, obj_in=random_entity_schema)
        assert is_schema_in_model(random_entity_schema, created_entity_model)

    def test_read_one_entity_service(
            self, db: Session, entity_service: BaseService, create_random_entity_schema, create_random_entity_with_service
    ) -> None:
        created_entity_model = create_random_entity_with_service(db)
        created_entity_model_id = created_entity_model.id
        read_entity_model = entity_service.read(db, id=created_entity_model_id)
        assert created_entity_model == read_entity_model

    def test_read_many_entities_service(
            self, db: Session, entity_service: BaseService, create_random_entity_schema, create_random_entity_with_service
    ) -> None:
        created_entity_model = create_random_entity_with_service(db)
        read_entity_model_list = entity_service.read_many(db)
        assert created_entity_model in read_entity_model_list

    def test_update_dummy_service(
            self, db: Session, entity_service: BaseService, create_random_entity_schema, create_random_entity_with_service
    ) -> None:
        created_entity_model = create_random_entity_with_service(db)
        created_entity_model_id = created_entity_model.id
        new_random_entity_schema = create_random_entity_schema(db)

        updated_entity_model = entity_service.update(
            db, id=created_entity_model_id, obj_in=new_random_entity_schema)

        assert is_schema_in_model(
            new_random_entity_schema, updated_entity_model)

    def test_delete_dummy_service(
            self, db: Session, entity_service: BaseService, create_random_entity_schema, create_random_entity_with_service
    ) -> None:
        created_entity_model = create_random_entity_with_service(db)
        created_entity_model_id = created_entity_model.id
        assert entity_service.delete(db, id=created_entity_model_id)

        read_entity_model = entity_service.read(db, id=created_entity_model_id)
        assert not read_entity_model

    def test_fail_to_delete_entity_service_with_non_existing_id(
            self, db: Session, entity_service: BaseService, create_random_entity_schema, create_random_entity_with_service
    ) -> None:
        wrong_entity_model_id = -1
        assert not entity_service.delete(db, id=wrong_entity_model_id)


# def test_init_private_service(db: Session) -> None:
#     assert _dummy_service
