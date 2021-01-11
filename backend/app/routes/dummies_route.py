from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routes.base_route import base_route
from ..tests.utils.dummy_utils import (DummyCreateSchema, DummyReadSchema,
                                       dummy_service)

dummies_route = APIRouter()

base_route(dummies_route,  route_paths.ROUTE_DUMMIES, "dummies", "dummy", dummy_service,
           DummyCreateSchema, DummyReadSchema)
