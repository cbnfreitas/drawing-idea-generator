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
            self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        random_entity_dict = create_random_entity_dict()
        created_entity_router_response = client.post(
            resource_path, json=random_entity_dict)

        assert is_success_code_response(created_entity_router_response)
        assert is_dict_in_response(
            random_entity_dict, created_entity_router_response)

    @see_also(base_route)
    def test_read_one_entity_router(
            self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        random_entity_model = create_random_entity_with_service(db)
        random_id = random_entity_model.id
        read_entity_router_response = client.get(
            f"{resource_path}/{random_id}")

        assert is_success_code_response(read_entity_router_response)
        assert (model_to_dict(random_entity_model) ==
                read_entity_router_response.json())

    @see_also(base_route)
    def test_fail_to_read_one_entity_router_with_non_existing_id(
        self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        wrong_entity_model_id = -1
        read_entity_router_response = client.get(
            f"{resource_path}/{wrong_entity_model_id}")

        assert read_entity_router_response.status_code == status.HTTP_404_NOT_FOUND

    @see_also(base_route)
    def test_read_many_entity_route(
            self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        random_entity_model = create_random_entity_with_service(db)
        read_entity_list_router_response = client.get(resource_path)

        assert is_success_code_response(read_entity_list_router_response)
        assert (model_to_dict(random_entity_model)
                in read_entity_list_router_response.json())

    @see_also(base_route)
    def test_update_entity_router(
            self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        entity_model = create_random_entity_with_service(db)
        entity_id = entity_model.id
        new_entity_dict = create_random_entity_dict()

        updated_entity_router_response = client.put(
            f"{resource_path}/{entity_id}", json=new_entity_dict)

        assert is_success_code_response(updated_entity_router_response)
        assert is_dict_in_response(
            new_entity_dict, updated_entity_router_response)

    def test_fail_to_update_entity_router_with_non_existing_id(
        self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        wrong_entity_model_id = -1
        new_entity_dict = create_random_entity_dict()

        updated_entity_router_response = client.put(
            f"{resource_path}/{wrong_entity_model_id}", json=new_entity_dict)

        assert updated_entity_router_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_entity_router(
            self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        entity_model = create_random_entity_with_service(db)
        entity_id = entity_model.id
        deleted_entity_router_response = client.delete(
            f"{resource_path}/{entity_id}")

        assert is_success_code_response(deleted_entity_router_response)

    def test_fail_to_delete_dummy_router_with_non_existing_id(
        self, client: TestClient, db: Session, resource_path, create_random_entity_dict, create_random_entity_with_service
    ) -> None:
        wrong_entity_model_id = -1
        deleted_entity_router_response = client.delete(
            f"{resource_path}/{wrong_entity_model_id}")

        assert deleted_entity_router_response.status_code == status.HTTP_404_NOT_FOUND
