from typing import Dict

from app.core import route_paths
from app.services.user_service import user_service
from app.tests.utils.rank_utils import (create_random_rank_dict,
                                        create_random_rank_schema,
                                        create_random_rank_with_service)
from fastapi.testclient import TestClient
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, class_mapper

from ..utils import (assert_success_and_get_dict, is_http_error,
                     is_success_code, model_to_dict, random_email,
                     random_lower_string)
from ..utils.user_utils import create_or_update_user_via_service


def test_create_rank_router(
        client: TestClient, db: Session
) -> None:
    random_rank_dict = create_random_rank_dict()
    created_rank_router_dict = assert_success_and_get_dict(client.post(
        route_paths.ROUTE_RANKS, json=random_rank_dict))
    assert random_rank_dict.items() <= created_rank_router_dict.items()


def test_read_rank_router(
        client: TestClient, db: Session
) -> None:
    random_rank_db = create_random_rank_with_service(db)
    rank_id = random_rank_db.id
    read_rank_router_dict = assert_success_and_get_dict(client.get(
        f"{route_paths.ROUTE_RANKS}/{rank_id}"))
    random_rank_db_dict = model_to_dict(random_rank_db)
    assert random_rank_db_dict == read_rank_router_dict


def test_read_many_rank_router(
        client: TestClient, db: Session
) -> None:
    random_rank_db = create_random_rank_with_service(db)
    read_rank_router_dict = assert_success_and_get_dict(client.get(
        route_paths.ROUTE_RANKS))
    random_rank_db_dict = model_to_dict(random_rank_db)
    assert random_rank_db_dict in read_rank_router_dict


# def test_update_user(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:

#     user = create_or_update_user_via_service(db)
#     user_id = user.id
#     full_name = random_lower_string()
#     data = {"full_name": full_name}
#     response = client.put(f"{route_paths.ROUTE_USERS}/{user_id}",
#                           headers=admin_token_headers, json=data)

#     assert is_success_code(response)
#     response = response.json()
#     assert response["full_name"] == full_name


# def test_fail_to_update_user_with_id_not_found(
#         client: TestClient, admin_token_headers: Dict[str, str]
# ) -> None:

#     user_id = 99999
#     full_name = random_lower_string()
#     data = {"full_name": full_name}
#     response = client.put(f"{route_paths.ROUTE_USERS}/{user_id}",
#                           headers=admin_token_headers, json=data)

#     assert is_http_error(response)


# def test_fail_to_update_user_with_email_already_in_use(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:

#     user1 = create_or_update_user_via_service(db)
#     user2 = create_or_update_user_via_service(db)
#     user2_id = user2.id
#     data = {"email": user1.email}
#     response = client.put(f"{route_paths.ROUTE_USERS}/{user2_id}",
#                           headers=admin_token_headers, json=data)

#     assert is_http_error(response)


# def test_read_user_from_id(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:
#     user = create_or_update_user_via_service(db)
#     user_id = user.id
#     response = client.get(f"{route_paths.ROUTE_USERS}/{user_id}",
#                           headers=admin_token_headers)
#     assert is_success_code(response)

#     api_user = response.json()
#     assert user.email == api_user["email"]


# def test_read_user_by_admin(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:
#     create_or_update_user_via_service(db)
#     create_or_update_user_via_service(db)

#     response = client.get(route_paths.ROUTE_USERS, headers=admin_token_headers)
#     assert is_success_code(response)

#     all_users = response.json()
#     assert len(all_users) >= 2
#     for user in all_users:
#         assert "email" in user


# def test_remove_user(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:
#     user = create_or_update_user_via_service(db)
#     user_id = user.id
#     response = client.delete(
#         f"{route_paths.ROUTE_USERS}/{user_id}", headers=admin_token_headers)
#     assert is_success_code(response)


# def test_fail_to_remove_user_with_id_not_found(
#         client: TestClient, admin_token_headers: Dict[str, str]
# ) -> None:
#     user_id_too_high_to_exist = 999999
#     response = client.delete(
#         f"{route_paths.ROUTE_USERS}/{user_id_too_high_to_exist}", headers=admin_token_headers)
#     assert is_http_error(response)
