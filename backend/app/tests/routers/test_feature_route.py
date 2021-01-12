import pytest

from ...core import route_paths
from ..utils.feature_utils import (create_random_feature_dict,
                                   create_random_feature_with_service)
from .test_base_route import _TestBaseRoute


@pytest.mark.parametrize("resource_path, create_random_entity_dict, create_random_entity_with_service",
                         [(route_paths.ROUTE_FEATURE, create_random_feature_dict, create_random_feature_with_service)])
class TestFeatureRoute(_TestBaseRoute):
    pass
