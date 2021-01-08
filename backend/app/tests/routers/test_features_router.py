from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ...core import route_paths
from ..utils import (is_dict_in_response, is_success_code_response,
                     model_to_dict)
from ..utils.feature_utils import (create_random_feature_dict,
                                   create_random_feature_with_service)


def test_create_feature_router(
        client: TestClient, db: Session
) -> None:
    random_feature_dict = create_random_feature_dict()
    created_feature_router_response = client.post(
        route_paths.ROUTE_FEATURES, json=random_feature_dict)

    assert is_success_code_response(created_feature_router_response)
    assert is_dict_in_response(
        random_feature_dict, created_feature_router_response)


def test_read_one_feature_router(
        client: TestClient, db: Session
) -> None:
    random_feature_model = create_random_feature_with_service(db)
    feature_id = random_feature_model.id
    read_feature_router_response = client.get(
        f"{route_paths.ROUTE_FEATURES}/{feature_id}")

    assert is_success_code_response(read_feature_router_response)
    assert (model_to_dict(random_feature_model) ==
            read_feature_router_response.json())


def test_fail_to_read_one_feature_router_with_non_existing_id(db: Session, client: TestClient) -> None:
    wrong_feature_model_id = -1
    read_feature_router_response = client.get(
        f"{route_paths.ROUTE_FEATURES}/{wrong_feature_model_id}")

    assert read_feature_router_response.status_code == status.HTTP_404_NOT_FOUND


def test_read_many_features_router(
        client: TestClient, db: Session
) -> None:
    random_feature_model = create_random_feature_with_service(db)
    read_feature_list_router_response = client.get(route_paths.ROUTE_FEATURES)

    assert is_success_code_response(read_feature_list_router_response)
    assert (model_to_dict(random_feature_model)
            in read_feature_list_router_response.json())


def test_update_feature_router(
        client: TestClient, db: Session
) -> None:
    feature_model = create_random_feature_with_service(db)
    feature_id = feature_model.id
    new_feature_dict = create_random_feature_dict()

    updated_feature_router_response = client.put(
        f"{route_paths.ROUTE_FEATURES}/{feature_id}", json=new_feature_dict)

    assert is_success_code_response(updated_feature_router_response)
    assert is_dict_in_response(
        new_feature_dict, updated_feature_router_response)


def test_fail_to_update_feature_router_with_non_existing_id(db: Session, client: TestClient) -> None:
    wrong_feature_model_id = -1
    new_feature_dict = create_random_feature_dict()

    updated_feature_router_response = client.put(
        f"{route_paths.ROUTE_FEATURES}/{wrong_feature_model_id}", json=new_feature_dict)

    assert updated_feature_router_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_feature_router(
        client: TestClient, db: Session
) -> None:
    feature_model = create_random_feature_with_service(db)
    feature_id = feature_model.id
    deleted_feature_router_response = client.delete(
        f"{route_paths.ROUTE_FEATURES}/{feature_id}")

    assert is_success_code_response(deleted_feature_router_response)


def test_fail_to_delete_feature_router_with_non_existing_id(db: Session, client: TestClient) -> None:
    wrong_feature_model_id = -1
    deleted_feature_router_response = client.delete(
        f"{route_paths.ROUTE_FEATURES}/{wrong_feature_model_id}")

    assert deleted_feature_router_response.status_code == status.HTTP_404_NOT_FOUND
