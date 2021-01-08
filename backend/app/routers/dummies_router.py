from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routers.base_router import build_simple_crud
from ..schemas.dummy_schema import DummyCreateSchema, DummyReadSchema
from ..services import dummy_service

dummies_router = APIRouter()

build_simple_crud(dummies_router,  route_paths.ROUTE_DUMMIES, "dummies", "dummy", dummy_service,
                  DummyCreateSchema, DummyReadSchema)
