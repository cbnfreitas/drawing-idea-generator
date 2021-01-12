import pytest

from ...core import route_paths
from ..utils.dummy_utils import (create_random_dummy_dict,
                                 create_random_dummy_schema,
                                 create_random_dummy_with_service)
from .test_base_route import _TestBaseRoute


@pytest.mark.parametrize("create_random_entity_dict, resource_path",
                         [(create_random_dummy_dict, route_paths.ROUTE_DUMMY)])
class TestDummyRoute(_TestBaseRoute):
    pass
