from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routers.base_router import build_simple_crud
from ..schemas.feature_schema import FeatureCreateSchema, FeatureReadSchema
from ..services import feature_service

features_router = APIRouter()

build_simple_crud(features_router,  route_paths.ROUTE_FEATURES, "features", "feature", feature_service,
                  FeatureCreateSchema, FeatureReadSchema)
