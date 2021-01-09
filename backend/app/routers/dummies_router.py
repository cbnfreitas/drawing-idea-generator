from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routers.base_router import base_router
from ..schemas.dummy_schema import DummyCreateSchema, DummyReadSchema
from ..tests.utils.dummy_utils import dummy_service

dummies_router = APIRouter()

base_router(dummies_router,  route_paths.ROUTE_DUMMIES, "dummies", "dummy", dummy_service,
            DummyCreateSchema, DummyReadSchema)
