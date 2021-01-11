from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routers.base_router import base_router
from ..schemas.feature_schema import FeatureCreateSchema, FeatureReadSchema
from ..services import value_service

values_router = APIRouter()

base_router(values_router,  route_paths.ROUTE_VALUES, "values", "values", value_service,
            FeatureCreateSchema, FeatureReadSchema)
