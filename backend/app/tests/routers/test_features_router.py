from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, class_mapper

from ...core import route_paths
from ...services.user_service import user_service
from ..utils import (is_dict_in_dict, is_dict_in_response,
                     is_error_code_response, is_success_code_response,
                     model_to_dict, random_email, random_lower_string)
from ..utils.feature_utils import (create_random_feature_dict,
                                   create_random_feature_with_service)
from ..utils.user_utils import create_or_update_user_via_service


def test_create_feature_router(
        client: TestClient, db: Session
) -> None:
    random_feature_dict = create_random_feature_dict()
    created_feature_router_response = client.post(
        route_paths.ROUTE_FEATURES, json=random_feature_dict)

    assert is_success_code_response(created_feature_router_response)
    assert is_dict_in_response(
        random_feature_dict, created_feature_router_response)


def test_read_feature_router(
        client: TestClient, db: Session
) -> None:
    random_feature_model = create_random_feature_with_service(db)
    feature_id = random_feature_model.id
    read_feature_router_response = client.get(
        f"{route_paths.ROUTE_FEATURES}/{feature_id}")

    assert is_success_code_response(read_feature_router_response)
    assert read_feature_router_response.json() == model_to_dict(random_feature_model)


# def test_read_many_rank_router(
#         client: TestClient, db: Session
# ) -> None:
#     random_rank_db = create_random_rank_with_service(db)
#     read_rank_router_dict = assert_success_and_get_dict(client.get(
#         route_paths.ROUTE_RANKS))
#     random_rank_db_dict = model_to_dict(random_rank_db)
#     assert random_rank_db_dict in read_rank_router_dict


# def test_update_user(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:

#     user = create_or_update_user_via_service(db)
#     user_id = user.id
#     full_name = random_lower_string()
#     data = {"full_name": full_name}
#     response = client.put(f"{route_paths.ROUTE_USERS}/{user_id}",
#                           headers=admin_token_headers, json=data)

#     assert is_success_code_response(response)
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

#     assert is_error_code_response(response)


# def test_fail_to_update_user_with_email_already_in_use(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:

#     user1 = create_or_update_user_via_service(db)
#     user2 = create_or_update_user_via_service(db)
#     user2_id = user2.id
#     data = {"email": user1.email}
#     response = client.put(f"{route_paths.ROUTE_USERS}/{user2_id}",
#                           headers=admin_token_headers, json=data)

#     assert is_error_code_response(response)


# def test_read_user_from_id(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:
#     user = create_or_update_user_via_service(db)
#     user_id = user.id
#     response = client.get(f"{route_paths.ROUTE_USERS}/{user_id}",
#                           headers=admin_token_headers)
#     assert is_success_code_response(response)

#     api_user = response.json()
#     assert user.email == api_user["email"]


# def test_read_user_by_admin(
#         client: TestClient, admin_token_headers: Dict[str, str], db: Session
# ) -> None:
#     create_or_update_user_via_service(db)
#     create_or_update_user_via_service(db)

#     response = client.get(route_paths.ROUTE_USERS, headers=admin_token_headers)
#     assert is_success_code_response(response)

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
#     assert is_success_code_response(response)


# def test_fail_to_remove_user_with_id_not_found(
#         client: TestClient, admin_token_headers: Dict[str, str]
# ) -> None:
#     user_id_too_high_to_exist = 999999
#     response = client.delete(
#         f"{route_paths.ROUTE_USERS}/{user_id_too_high_to_exist}", headers=admin_token_headers)
#     assert is_error_code_response(response)
