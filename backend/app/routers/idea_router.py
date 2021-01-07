from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import route_paths
from ..core.depends import get_db, get_user_from_access_token
from ..routers.users_router import update_user_by_helper
from ..schemas.msg_schema import MsgResponseSchema
from ..schemas.user_schema import UserReadSchema, UserUpdateSchema
from ..services import user_service

router = APIRouter()


@router.get(route_paths.ROUTE_IDEAS, response_model=MsgResponseSchema)
def generate_random_idea(
        db: Session = Depends(get_db)
) -> Any:
    """
    Generate random idea.
    """
    return MsgResponseSchema(detail="Troll riding a bike")
