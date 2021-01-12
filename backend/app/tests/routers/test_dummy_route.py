import pytest

from ...core import route_paths
from ..utils.auth_utils import no_header
from ..utils.dummy_utils import (DummyReadSchema, create_random_dummy_dict,
                                 create_random_dummy_with_service)
from .test_base_route import _TestBaseRoute


@pytest.mark.parametrize("resource_path, create_random_entity_dict, create_random_entity_with_service, headers_builder",
                         [(route_paths.ROUTE_DUMMY, create_random_dummy_dict, create_random_dummy_with_service, no_header)])
class TestDummyRoute(_TestBaseRoute):
    pass
