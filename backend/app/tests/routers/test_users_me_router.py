from typing import Dict

from app.routes.users_me_route import (
    read_current_user_info_from_access_token, update_user_from_access_token)
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ...core import route_paths, s
from ..utils import is_success_code_response, random_lower_string, see_also
from ..utils.auth_utils import get_access_token_from_email
from ..utils.user_utils import create_or_update_user_via_service


@see_also(read_current_user_info_from_access_token)
def test_read_users_me_admin(
        client: TestClient, admin_token_headers: Dict[str, str]
) -> None:
    response = client.get(route_paths.ROUTE_USERS_ME,
                          headers=admin_token_headers)
    assert is_success_code_response(response)

    current_user = response.json()
    assert current_user
    assert current_user["is_admin"] == True
    assert current_user["email"] == s.FIRST_ADMIN


@see_also(read_current_user_info_from_access_token)
def test_read_users_me_normal(client: TestClient, db: Session) -> None:

    user = create_or_update_user_via_service(db)
    headers = get_access_token_from_email(db=db, email=user.email)

    response = client.get(route_paths.ROUTE_USERS_ME, headers=headers)
    assert is_success_code_response(response)

    current_user = response.json()
    assert current_user
    assert current_user["is_admin"] == False
    assert current_user["email"] == user.email


@see_also(update_user_from_access_token)
def test_update_me_full_name(
        client: TestClient, user_token_headers: Dict[str, str]
) -> None:

    full_name = random_lower_string()
    data = {"full_name": full_name}
    response = client.put(
        route_paths.ROUTE_USERS_ME, headers=user_token_headers, json=data)

    assert is_success_code_response(response)
    response = response.json()
    assert response["full_name"] == full_name
