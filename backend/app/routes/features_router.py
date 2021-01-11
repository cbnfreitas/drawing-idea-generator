from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routes.base_route import base_route
from ..schemas.feature_schema import FeatureCreateSchema, FeatureReadSchema
from ..services import feature_service

features_router = APIRouter()

base_route(features_router,  route_paths.ROUTE_FEATURES, "features", "feature", feature_service,
           FeatureCreateSchema, FeatureReadSchema)
