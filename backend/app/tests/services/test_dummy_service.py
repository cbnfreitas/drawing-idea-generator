import pytest
from sqlalchemy.orm import Session

from ...routes.base_route import base_route
from ...services.base_service import BaseService
from ..utils import is_schema_in_model, see_also
from ..utils.dummy_utils import (DummyCreateSchema, DummyModel,
                                 create_random_dummy_schema,
                                 create_random_dummy_with_service,
                                 dummy_service)
from .test_base_service import _TestBaseService


@pytest.mark.parametrize("entity_service, create_random_entity_schema, create_random_entity_with_service",
                         [(dummy_service, create_random_dummy_schema, create_random_dummy_with_service)])
class TestDummyService(_TestBaseService):
    def test_read_many_dummies_service_with_criteria(
            self, db: Session, entity_service: BaseService, create_random_entity_schema, create_random_entity_with_service
    ) -> None:

        created_entity_model_a = entity_service.create(
            db, obj_in=DummyCreateSchema(name='cool name a', stars=3))
        created_entity_model_b = entity_service.create(
            db, obj_in=DummyCreateSchema(name='cool name b', stars=3))

        read_entity_model_list_stars_3 = entity_service.read_many(
            db, criteria=(DummyModel.stars == 3))

        for entity in read_entity_model_list_stars_3:
            assert entity.stars == 3
