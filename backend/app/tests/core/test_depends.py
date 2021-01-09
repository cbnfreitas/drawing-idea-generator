import time

from app.schemas.user_schema import UserUpdateSchema
from fastapi.testclient import TestClient
from pytest import raises
from sqlalchemy.orm.session import Session

from ...core import error_msgs, s
from ...core.depends import (get_admin_from_access_token, get_db,
                             get_user_db_from_refresh_token,
                             get_user_from_access_token)
from ...core.security import create_refresh_token
from ...models.user_model import UserModel
from ...schemas.auth_schema import RefreshRequestSchema
from ...services import denied_token_redis, user_service
from ..utils import has_error_detail, random_email, random_integer
from ..utils.auth_utils import (get_access_token_from_email,
                                user_auth_headers_from_security,
                                user_auth_refresh_from_security)
from ..utils.user_utils import create_or_update_user_via_service


def test_get_db():
    db = get_db()
    assert db


def test_get_user_from_access_token(client: TestClient, db: Session):

    user = create_or_update_user_via_service(db)
    headers = get_access_token_from_email(db=db, email=user.email)
    token = headers['Authorization'].replace("Bearer ", "", 1)

    user_token_data = get_user_from_access_token(db=db, access_token=token)
    assert user_token_data
    assert user_token_data['user_id'] == user.id
    assert user_token_data['is_admin'] == user.is_admin


def test_fail_to_get_user_from_access_token_denied_token(client: TestClient, db: Session):

    user = create_or_update_user_via_service(db)
    headers = get_access_token_from_email(db=db, email=user.email)
    token = headers['Authorization'].replace("Bearer ", "", 1)
    denied_token_redis.set(token, "")

    with raises(Exception) as e:
        assert get_user_from_access_token(db=db, access_token=token)
    assert has_error_detail(e, error_msgs.DENIED_TOKEN)


def test_get_admin_from_access_token(db: Session, client: TestClient) -> None:
    user = user_service.read_by_email(db, email=s.FIRST_ADMIN)
    user_token_data = {'user_id': user.id, 'is_admin': user.is_admin}
    admin_token_data = get_admin_from_access_token(user_token_data)
    assert admin_token_data


def test_fail_to_get_admin_from_access_token_with_normal_user(db: Session, client: TestClient) -> None:
    any_id = random_integer()
    user_token_data = {'user_id': any_id, 'is_admin': False}

    with raises(Exception) as e:
        assert get_admin_from_access_token(admin_token_data=user_token_data)
    assert has_error_detail(e, error_msgs.ONLY_AVAILABLE_TO_ADMIN)


def test_get_user_db_from_refresh_token(db: Session):
    user = create_or_update_user_via_service(db)
    refresh_dict = user_auth_refresh_from_security(user_id=user.id)
    refresh_body = RefreshRequestSchema(**refresh_dict)

    user_db_token = get_user_db_from_refresh_token(
        db=db, refresh_body=refresh_body)
    assert user_db_token.id == user.id


def test_fail_get_user_db_from_refresh_token_expired_one_hour_ago(db: Session):
    user = create_or_update_user_via_service(db)
    refresh_token = create_refresh_token(user_id=user.id, exp_delta_hours=-1)
    refresh_body = RefreshRequestSchema(refresh_token=refresh_token)

    with raises(Exception) as e:
        assert get_user_db_from_refresh_token(db=db, refresh_body=refresh_body)
    assert has_error_detail(e, error_msgs.EXPIRED_TOKEN)


def test_fail_get_user_db_from_refresh_token_auth_change_after_one_milliseconds(db: Session):
    user = create_or_update_user_via_service(db)
    refresh_dict = user_auth_refresh_from_security(user_id=user.id)
    refresh_body = RefreshRequestSchema(**refresh_dict)

    new_email = random_email()
    time.sleep(.001)
    user_service.update(
        db, id=user.id, obj_in=UserUpdateSchema(email=new_email))

    with raises(Exception) as e:
        assert get_user_db_from_refresh_token(db=db, refresh_body=refresh_body)
    assert has_error_detail(e, error_msgs.STALE_CREDENTIALS)
