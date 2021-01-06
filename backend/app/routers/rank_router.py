from typing import Any

from fastapi import APIRouter

from ..schemas.rank_schema import RankRequestSchema, RankResponseSchema
from ..services.rank_service import rank_service
from .base_router import build_simple_crud

rank_router = APIRouter()

# TODO add variables to hold rank, ranks
build_simple_crud(rank_router,  "rank", "ranks", rank_service,
                  RankRequestSchema, RankResponseSchema)
