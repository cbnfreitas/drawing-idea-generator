from http import HTTPStatus
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from ..core import route_paths
from ..routes.base_route import base_route
from ..schemas.value_schema import ValueCreateSchema, ValueReadSchema
from ..services import value_service

value_route = APIRouter()

base_route(value_route,  route_paths.ROUTE_VALUE, "values", "values", value_service,
           ValueCreateSchema, ValueReadSchema)
