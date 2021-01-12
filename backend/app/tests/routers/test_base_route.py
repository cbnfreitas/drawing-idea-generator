from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ...routes.base_route import base_route
from ..utils import (is_dict_in_dict, is_dict_in_response,
                     is_model_in_response, is_success_code_response,
                     model_to_dict, see_also)


class _TestBaseRoute:
    @see_also(base_route)
    def test_create_entity_router(
            self, client: TestClient, db: Session,
            resource_path, create_random_entity_dict, create_random_entity_with_service,
            headers_builder
    ) -> None:
        random_entity_dict = create_random_entity_dict(db)
        headers = headers_builder(db)
        created_entity_router_response = client.post(
            resource_path, headers=headers, json=random_entity_dict)

        assert is_success_code_response(created_entity_router_response)
        assert is_dict_in_response(
            random_entity_dict, created_entity_router_response)

    @see_also(base_route)
    def test_read_one_entity_router(
            self, client: TestClient, db: Session,
            resource_path, create_random_entity_dict, create_random_entity_with_service,
            headers_builder
    ) -> None:
        random_entity_model = create_random_entity_with_service(db)
        random_id = random_entity_model.id
        headers = headers_builder(db)
        read_entity_router_response = client.get(
            f"{resource_path}/{random_id}", headers=headers)

        assert is_success_code_response(read_entity_router_response)
        assert is_model_in_response(
            random_entity_model, read_entity_router_response)

    @see_also(base_route)
    def test_fail_to_read_one_entity_router_with_non_existing_id(
        self, client: TestClient, db: Session,
        resource_path, create_random_entity_dict, create_random_entity_with_service,
        headers_builder
    ) -> None:
        wrong_entity_model_id = -1
        headers = headers_builder(db)
        read_entity_router_response = client.get(
            f"{resource_path}/{wrong_entity_model_id}", headers=headers)

        assert read_entity_router_response.status_code == status.HTTP_404_NOT_FOUND

    @see_also(base_route)
    def test_read_many_entity_route(
            self, client: TestClient, db: Session,
            resource_path, create_random_entity_dict, create_random_entity_with_service,
            headers_builder
    ) -> None:
        random_entity_model = create_random_entity_with_service(db)
        headers = headers_builder(db)
        read_entity_list_router_response = client.get(
            resource_path, headers=headers)
        assert is_success_code_response(read_entity_list_router_response)

        last_entity_on_response = read_entity_list_router_response.json()[-1]
        random_entity_model_dict = model_to_dict(random_entity_model)
        assert is_dict_in_dict(random_entity_model_dict,
                               last_entity_on_response)

    @see_also(base_route)
    def test_update_entity_router(
            self, client: TestClient, db: Session,
            resource_path, create_random_entity_dict, create_random_entity_with_service,
            headers_builder
    ) -> None:
        entity_model = create_random_entity_with_service(db)
        entity_id = entity_model.id
        new_entity_dict = create_random_entity_dict(db)

        headers = headers_builder(db)
        updated_entity_router_response = client.put(
            f"{resource_path}/{entity_id}", headers=headers, json=new_entity_dict)

        assert is_success_code_response(updated_entity_router_response)
        assert is_dict_in_response(
            new_entity_dict, updated_entity_router_response)

    def test_fail_to_update_entity_router_with_non_existing_id(
        self, client: TestClient, db: Session,
        resource_path, create_random_entity_dict, create_random_entity_with_service,
        headers_builder
    ) -> None:
        wrong_entity_model_id = -1
        new_entity_dict = create_random_entity_dict(db)

        headers = headers_builder(db)
        updated_entity_router_response = client.put(
            f"{resource_path}/{wrong_entity_model_id}", headers=headers, json=new_entity_dict)

        assert updated_entity_router_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_entity_router(
            self, client: TestClient, db: Session,
            resource_path, create_random_entity_dict, create_random_entity_with_service,
            headers_builder
    ) -> None:
        entity_model = create_random_entity_with_service(db)
        entity_id = entity_model.id

        headers = headers_builder(db)
        deleted_entity_router_response = client.delete(
            f"{resource_path}/{entity_id}", headers=headers)

        assert is_success_code_response(deleted_entity_router_response)

    def test_fail_to_delete_dummy_router_with_non_existing_id(
        self, client: TestClient, db: Session,
        resource_path, create_random_entity_dict, create_random_entity_with_service,
        headers_builder
    ) -> None:
        wrong_entity_model_id = -1
        headers = headers_builder(db)
        deleted_entity_router_response = client.delete(
            f"{resource_path}/{wrong_entity_model_id}", headers=headers)

        assert deleted_entity_router_response.status_code == status.HTTP_404_NOT_FOUND
