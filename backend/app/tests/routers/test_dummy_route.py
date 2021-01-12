import pytest

from ...core import route_paths
from ..utils.dummy_utils import (create_random_dummy_dict,
                                 create_random_dummy_with_service)
from .test_base_route import _TestBaseRoute


@pytest.mark.parametrize("resource_path, create_random_entity_dict, create_random_entity_with_service",
                         [(route_paths.ROUTE_DUMMY, create_random_dummy_dict, create_random_dummy_with_service)])
class TestDummyRoute(_TestBaseRoute):
    pass
