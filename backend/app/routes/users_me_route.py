from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core import route_paths
from ..core.depends import get_db, get_user_from_access_token
from ..routes.users_route import update_user_by_helper
from ..schemas.user_schema import UserReadSchema, UserUpdateSchema
from ..services import user_service

router = APIRouter()


@router.get(route_paths.ROUTE_USERS_ME, response_model=UserReadSchema)
def read_current_user_info_from_access_token(
        db: Session = Depends(get_db),
        user_token_data: Dict[str, Any] = Depends(get_user_from_access_token),
) -> Any:
    """
    Get current user.
    """
    user = user_service.read(db, id=user_token_data['user_id'])
    return user


@router.put(route_paths.ROUTE_USERS_ME, response_model=UserReadSchema)
def update_user_from_access_token(
        db: Session = Depends(get_db),
        user_token_data: Dict[str, Any] = Depends(get_user_from_access_token),
        *,
        user_in: UserUpdateSchema
) -> Any:
    """
    Update own user.
    """
    user = update_user_by_helper(
        db, user_id=user_token_data["user_id"], user_in=user_in)
    return user
