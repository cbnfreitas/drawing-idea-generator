from typing import Any, Dict

from app.services import feature_service
from app.tests.utils import random_integer
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import route_paths
from ..core.depends import get_db
from ..schemas.msg_schema import MsgResponseSchema

idea_route = APIRouter()


@idea_route.get(route_paths.ROUTE_IDEA, response_model=MsgResponseSchema)
def generate_random_idea(
        db: Session = Depends(get_db)
) -> Any:
    """
    Generate random idea.
    """

    features = feature_service.read_many(db)
    idea = ""
    for feature in features:
        random_value_index = random_integer(min=0, max=len(feature.values) - 1)
        random_value = feature.values[random_value_index].value
        idea = f"{idea}{random_value} "

    return MsgResponseSchema(detail=idea.strip())
