import pytest

from ..utils.dummy_utils import (create_random_dummy_schema,
                                 create_random_dummy_with_service,
                                 dummy_service)
from .test_base_service import _TestBaseService


@pytest.mark.parametrize("entity_service, create_random_entity_schema, create_random_entity_with_service",
                         [(dummy_service, create_random_dummy_schema, create_random_dummy_with_service)])
class TestBaseServiceDummy(_TestBaseService):
    pass
