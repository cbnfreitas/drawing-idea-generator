import pytest

from ...services import value_service
from ..utils.value_utils import (create_random_value_schema,
                                 create_random_value_with_service)
from .test_base_service import _TestBaseService


@pytest.mark.parametrize("entity_service, create_random_entity_schema, create_random_entity_with_service",
                         [(value_service, create_random_value_schema, create_random_value_with_service)])
class TestValueService(_TestBaseService):
    pass
