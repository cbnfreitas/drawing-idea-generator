import pytest

from ...core import route_paths
from ..utils.auth_utils import get_access_token_first_admin
from ..utils.feature_utils import (create_random_feature_dict,
                                   create_random_feature_with_service)
from .test_base_route import _TestBaseRoute


@pytest.mark.parametrize("resource_path, create_random_entity_dict, create_random_entity_with_service, headers_builder",
                         [(route_paths.ROUTE_FEATURE, create_random_feature_dict, create_random_feature_with_service, get_access_token_first_admin)])
class TestFeatureRoute(_TestBaseRoute):
    pass
