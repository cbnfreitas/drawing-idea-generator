import pytest

from ...services import feature_service
from ..utils.feature_utils import (create_random_feature_schema,
                                   create_random_feature_with_service)
from .test_base_service import _TestBaseService


@pytest.mark.parametrize("entity_service, create_random_entity_schema, create_random_entity_with_service",
                         [(feature_service, create_random_feature_schema, create_random_feature_with_service)])
class TestBaseServiceFeature(_TestBaseService):
    pass
