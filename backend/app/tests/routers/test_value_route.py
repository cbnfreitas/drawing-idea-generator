import pytest

from ...core import route_paths
from ..utils.auth_utils import no_header
from ..utils.value_utils import (create_random_value_dict,
                                 create_random_value_with_service)
from .test_base_route import _TestBaseRoute


@pytest.mark.parametrize("resource_path, create_random_entity_dict, create_random_entity_with_service, headers_builder",
                         [(route_paths.ROUTE_VALUE, create_random_value_dict, create_random_value_with_service, no_header)])
class TestValueRoute(_TestBaseRoute):
    pass
