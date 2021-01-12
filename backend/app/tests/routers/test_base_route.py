from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ...routes.base_route import base_route
from ..utils import (is_dict_in_response, is_success_code_response,
                     model_to_dict, see_also)


class _TestBaseRoute:

    @see_also(base_route)
    def test_create_entity_router(
            self, client: TestClient, db: Session, create_random_entity_dict, resource_path
    ) -> None:
        random_entity_dict = create_random_entity_dict()
        created_entity_router_response = client.post(
            resource_path, json=random_entity_dict)

        assert is_success_code_response(created_entity_router_response)
        assert is_dict_in_response(
            random_entity_dict, created_entity_router_response)


# def test_read_one_dummy_router(
#         client: TestClient, db: Session
# ) -> None:
#     random_dummy_model = create_random_dummy_with_service(db)
#     dummy_id = random_dummy_model.id
#     read_dummy_router_response = client.get(
#         f"{route_paths.ROUTE_DUMMY}/{dummy_id}")

#     assert is_success_code_response(read_dummy_router_response)
#     assert (model_to_dict(random_dummy_model) ==
#             read_dummy_router_response.json())


# def test_fail_to_read_one_dummy_router_with_non_existing_id(db: Session, client: TestClient) -> None:
#     wrong_dummy_model_id = -1
#     read_dummy_router_response = client.get(
#         f"{route_paths.ROUTE_DUMMY}/{wrong_dummy_model_id}")

#     assert read_dummy_router_response.status_code == status.HTTP_404_NOT_FOUND


# def test_read_many_dummy_route(
#         client: TestClient, db: Session
# ) -> None:
#     random_dummy_model = create_random_dummy_with_service(db)
#     read_dummy_list_router_response = client.get(route_paths.ROUTE_DUMMY)

#     assert is_success_code_response(read_dummy_list_router_response)
#     assert (model_to_dict(random_dummy_model)
#             in read_dummy_list_router_response.json())


# def test_update_dummy_router(
#         client: TestClient, db: Session
# ) -> None:
#     dummy_model = create_random_dummy_with_service(db)
#     dummy_id = dummy_model.id
#     new_dummy_dict = create_random_dummy_dict()

#     updated_dummy_router_response = client.put(
#         f"{route_paths.ROUTE_DUMMY}/{dummy_id}", json=new_dummy_dict)

#     assert is_success_code_response(updated_dummy_router_response)
#     assert is_dict_in_response(
#         new_dummy_dict, updated_dummy_router_response)


# def test_fail_to_update_dummy_router_with_non_existing_id(db: Session, client: TestClient) -> None:
#     wrong_dummy_model_id = -1
#     new_dummy_dict = create_random_dummy_dict()

#     updated_dummy_router_response = client.put(
#         f"{route_paths.ROUTE_DUMMY}/{wrong_dummy_model_id}", json=new_dummy_dict)

#     assert updated_dummy_router_response.status_code == status.HTTP_404_NOT_FOUND


# def test_delete_dummy_router(
#         client: TestClient, db: Session
# ) -> None:
#     dummy_model = create_random_dummy_with_service(db)
#     dummy_id = dummy_model.id
#     deleted_dummy_router_response = client.delete(
#         f"{route_paths.ROUTE_DUMMY}/{dummy_id}")

#     assert is_success_code_response(deleted_dummy_router_response)


# def test_fail_to_delete_dummy_router_with_non_existing_id(db: Session, client: TestClient) -> None:
#     wrong_dummy_model_id = -1
#     deleted_dummy_router_response = client.delete(
#         f"{route_paths.ROUTE_DUMMY}/{wrong_dummy_model_id}")

#     assert deleted_dummy_router_response.status_code == status.HTTP_404_NOT_FOUND
