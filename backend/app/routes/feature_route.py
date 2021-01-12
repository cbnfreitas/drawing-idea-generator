from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routes.base_route import base_route
from ..schemas.feature_schema import FeatureCreateSchema, FeatureReadSchema
from ..services import feature_service

feature_route = APIRouter()

base_route(feature_route,  route_paths.ROUTE_FEATURE, "features", "feature", feature_service,
           FeatureCreateSchema, FeatureReadSchema)
