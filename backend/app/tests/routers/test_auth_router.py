from app.schemas.user_schema import UserCreateSchema
from fastapi.testclient import TestClient
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from ...core import error_msgs, route_paths
from ...core.security import create_password_reset_token, decode_sub_jwt
from ...routers.auth_router import registration
from ...services.user_service import user_service
from ..utils import (is_error_code_response, is_success_code_response,
                     random_email, random_lower_string)
from ..utils.auth_utils import (get_access_token_from_email,
                                user_auth_refresh_from_security)
from ..utils.user_utils import create_or_update_user_via_service


def test_register_router(client: TestClient, db: Session) -> None:

    registration_data = UserCreateSchema(
        email=random_email(), password=random_lower_string()).dict()

    response = client.post(
        route_paths.ROUTE_AUTH_REGISTER_AND_ACTIVATION_TOKEN_TO_EMAIL, json=registration_data)
    assert is_success_code_response(response)


def test_failt_to_register_router_email_already_in_use(client: TestClient, db: Session) -> None:
    user = create_or_update_user_via_service(db)
    registration_data = UserCreateSchema(
        email=user.email, password=random_lower_string()).dict()

    response = client.post(
        route_paths.ROUTE_AUTH_REGISTER_AND_ACTIVATION_TOKEN_TO_EMAIL, json=registration_data)

    assert is_error_code_response(
        response, error_msgs.EMAIL_ALREADY_IN_USE)


def test_login(client: TestClient, db: Session) -> None:

    password = random_lower_string()
    user = create_or_update_user_via_service(db, password=password)
    login_data = {"username": user.email, "password": password}

    response = client.post(route_paths.ROUTE_AUTH_LOGIN, data=login_data)
    assert is_success_code_response(response)
    tokens = response.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]


def test_fail_to_login_wrong_password(client: TestClient, db: Session) -> None:
    user = create_or_update_user_via_service(db)
    wrong_password = random_lower_string()
    login_data = {"username": user.email, "password": wrong_password}

    response = client.post(route_paths.ROUTE_AUTH_LOGIN, data=login_data)
    assert is_error_code_response(
        response, error_msgs.INCORRECT_EMAIL_OR_PASSWORD)
    tokens = response.json()
    assert "access_token" not in tokens


def test_login_refresh_and_check_new_access_token(client: TestClient, db: Session) -> None:

    user = create_or_update_user_via_service(db)
    refresh_body = user_auth_refresh_from_security(user_id=user.id)

    response = client.post(route_paths.ROUTE_AUTH_REFRESH, json=refresh_body)
    assert is_success_code_response(response)
    tokens = response.json()
    assert "access_token" in tokens
    decoded = decode_sub_jwt(db, tokens["access_token"])
    assert decoded["user_id"] == user.id
    assert decoded["is_admin"] == user.is_admin


def test_logout(client: TestClient, db: Session) -> None:

    any_user_token = get_access_token_from_email(db=db)
    response = client.post(route_paths.ROUTE_AUTH_LOGOUT,
                           headers=any_user_token)
    assert is_success_code_response(response)


def test_password_change_and_login(db: Session, client: TestClient) -> None:

    email = random_email()
    password = random_lower_string()
    token = get_access_token_from_email(db=db, email=email, password=password)

    new_password = random_lower_string()
    data_change_password = {
        "current_password": password, "new_password": new_password}
    response = client.post(route_paths.ROUTE_AUTH_PASSWORD_CHANGE,
                           headers=token,
                           json=data_change_password)
    assert is_success_code_response(response)

    login_data = {
        "username": email,
        "password": new_password,
    }
    response = client.post(route_paths.ROUTE_AUTH_LOGIN, data=login_data)
    assert is_success_code_response(response)


def test_fail_password_change_wrong_current_password(db: Session, client: TestClient) -> None:

    token = get_access_token_from_email(db=db)

    new_password = random_lower_string()
    wrong_current_password = random_lower_string()

    data_change_password = {
        "current_password": wrong_current_password, "new_password": new_password}
    response = client.post(route_paths.ROUTE_AUTH_PASSWORD_CHANGE,
                           headers=token,
                           json=data_change_password)

    assert is_error_code_response(
        response, error_msgs.INVALID_CURRENT_PASSWORD)


def test_password_reset_token(client: TestClient, db: Session) -> None:
    user = create_or_update_user_via_service(db)
    uri = f"{route_paths.ROUTE_AUTH_PASSWORD_RESET_TOKEN_TO_EMAIL}/{user.email}"
    response = client.post(uri)
    assert is_success_code_response(response)


def test_fail_to_password_token_email_not_found(client: TestClient) -> None:
    email = random_email()
    uri = f"{route_paths.ROUTE_AUTH_PASSWORD_RESET_TOKEN_TO_EMAIL}/{email}"
    response = client.post(uri)
    assert is_error_code_response(response, error_msgs.UNREGISTERED_EMAIL)


def test_password_reset_and_login(db: Session, client: TestClient) -> None:

    user = create_or_update_user_via_service(db)
    password_reset_token = create_password_reset_token(email=user.email)
    new_password = random_lower_string()

    data_change_password = {
        "reset_token": password_reset_token, "new_password": new_password}
    response = client.post(route_paths.ROUTE_AUTH_PASSWORD_RESET,
                           json=data_change_password)
    assert response
    assert is_success_code_response(response)

    login_data = {
        "username": user.email,
        "password": new_password,
    }
    response = client.post(route_paths.ROUTE_AUTH_LOGIN, data=login_data)
    assert is_success_code_response(response)


def test_fail_password_reset_expired_token_one_our_ago(db: Session, client: TestClient) -> None:
    user = create_or_update_user_via_service(db)
    password_reset_token = create_password_reset_token(
        email=user.email, exp_delta_hours=-1)
    new_password = random_lower_string()

    data_change_password = {
        "reset_token": password_reset_token, "new_password": new_password}

    response = client.post(route_paths.ROUTE_AUTH_PASSWORD_RESET,
                           json=data_change_password)
    assert is_error_code_response(response, error_msgs.EXPIRED_TOKEN)


def test_fail_password_reset_delete_user(db: Session, client: TestClient) -> None:

    user = create_or_update_user_via_service(db)
    password_reset_token = create_password_reset_token(email=user.email)
    new_password = random_lower_string()

    data_change_password = {
        "reset_token": password_reset_token, "new_password": new_password}

    user_service.delete(db, id=user.id)

    response = client.post(route_paths.ROUTE_AUTH_PASSWORD_RESET,
                           json=data_change_password)
    assert is_error_code_response(response, error_msgs.EMAIL_DOES_NOT_EXIST)
