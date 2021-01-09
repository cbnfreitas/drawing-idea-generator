from typing import Dict

from app.core import route_paths
from app.services.user_service import user_service
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..utils import (is_error_code_response, is_success_code_response,
                     random_email, random_lower_string)
from ..utils.user_utils import create_or_update_user_via_service


def test_create_user(
        client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = client.post(
        route_paths.ROUTE_USERS, headers=admin_token_headers, json=data)
    assert is_success_code_response(response)
    created_user = response.json()

    user = user_service.read_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_fail_to_create_user_with_existing_username(
        client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:
    previous_user = create_or_update_user_via_service(db)
    email_from_previous_user = previous_user.email
    password = random_lower_string()
    data = {"email": email_from_previous_user, "password": password}
    response = client.post(
        route_paths.ROUTE_USERS, headers=admin_token_headers, json=data)
    created_user = response.json()
    assert is_error_code_response(response)
    assert "_id" not in created_user


def test_fail_to_create_user_by_user(
        client: TestClient, user_token_headers: Dict[str, str]
) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    response = client.post(
        route_paths.ROUTE_USERS, headers=user_token_headers, json=data)
    assert is_error_code_response(response)


def test_update_user(
        client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:

    user = create_or_update_user_via_service(db)
    user_id = user.id
    full_name = random_lower_string()
    data = {"full_name": full_name}
    response = client.put(f"{route_paths.ROUTE_USERS}/{user_id}",
                          headers=admin_token_headers, json=data)

    assert is_success_code_response(response)
    response = response.json()
    assert response["full_name"] == full_name


def test_fail_to_update_user_with_id_not_found(
        client: TestClient, admin_token_headers: Dict[str, str]
) -> None:

    user_id = 99999
    full_name = random_lower_string()
    data = {"full_name": full_name}
    response = client.put(f"{route_paths.ROUTE_USERS}/{user_id}",
                          headers=admin_token_headers, json=data)

    assert is_error_code_response(response)


def test_fail_to_update_user_with_email_already_in_use(
        client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:

    user1 = create_or_update_user_via_service(db)
    user2 = create_or_update_user_via_service(db)
    user2_id = user2.id
    data = {"email": user1.email}
    response = client.put(f"{route_paths.ROUTE_USERS}/{user2_id}",
                          headers=admin_token_headers, json=data)

    assert is_error_code_response(response)


def test_read_user_from_id(
        client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:
    user = create_or_update_user_via_service(db)
    user_id = user.id
    response = client.get(f"{route_paths.ROUTE_USERS}/{user_id}",
                          headers=admin_token_headers)
    assert is_success_code_response(response)

    api_user = response.json()
    assert user.email == api_user["email"]


def test_read_user_by_admin(
        client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:
    create_or_update_user_via_service(db)
    create_or_update_user_via_service(db)

    response = client.get(route_paths.ROUTE_USERS, headers=admin_token_headers)
    assert is_success_code_response(response)

    all_users = response.json()
    assert len(all_users) >= 2
    for user in all_users:
        assert "email" in user


def test_remove_user(
        client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:
    user = create_or_update_user_via_service(db)
    user_id = user.id
    response = client.delete(
        f"{route_paths.ROUTE_USERS}/{user_id}", headers=admin_token_headers)
    assert is_success_code_response(response)


def test_fail_to_remove_user_with_id_not_found(
        client: TestClient, admin_token_headers: Dict[str, str]
) -> None:
    user_id_too_high_to_exist = 999999
    response = client.delete(
        f"{route_paths.ROUTE_USERS}/{user_id_too_high_to_exist}", headers=admin_token_headers)
    assert is_error_code_response(response)
