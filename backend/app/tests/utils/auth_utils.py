from typing import Dict

from sqlalchemy.orm import Session

from ...core.security import create_access_token, create_refresh_token
from ..utils import random_email
from ..utils.user_utils import create_or_update_user_via_service


def user_auth_headers_from_security(
        *, user_id: int, is_admin: bool
) -> Dict[str, str]:
    '''
    Create access token for a user.
    '''
    access_token = create_access_token(user_id=user_id, is_admin=is_admin)
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def user_auth_refresh_from_security(
        *, user_id: int
) -> Dict[str, str]:
    '''
    Create refresh token for a user.
    '''
    refresh_token = create_refresh_token(user_id=user_id)
    refresh_body = {"refresh_token": refresh_token}
    return refresh_body


def get_access_token_from_email(*,  db: Session, email: str = None, password: str = None) -> Dict[str, str]:
    """
    Return a valid token for the user. If the user doesn't exist, it is created.
    """
    if not email:
        email = random_email()

    user = create_or_update_user_via_service(
        db, email=email, password=password)

    return user_auth_headers_from_security(user_id=user.id, is_admin=user.is_admin)
