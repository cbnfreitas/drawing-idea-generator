from app.core.security import (create_access_token,
                               create_password_reset_token,
                               create_refresh_token, decode_sub_jwt,
                               encode_sub_exp_jwt, get_password_hash,
                               verify_password)
from pytest import raises
from sqlalchemy.orm import Session

from ...services import denied_token_redis
from ..utils import (random_boolean, random_email, random_integer,
                     random_lower_string)


def test_get_password_hash_and_verify_password():
    password = random_lower_string()
    hash_password = get_password_hash(password)
    assert verify_password(password, hash_password)


def test_encode_decode_sub_jwt(db: Session):
    value = random_lower_string()
    sub = {"key": value}
    token = encode_sub_exp_jwt(sub)
    sub_decode = decode_sub_jwt(db, token)
    assert sub.items() <= sub_decode.items()


def test_fail_to_decode_invalid_signature(db: Session):
    value = random_lower_string()
    sub = {"key": value}
    wrong_secret = random_lower_string()
    token = encode_sub_exp_jwt(sub, secret=wrong_secret)
    with raises(Exception) as e:
        assert decode_sub_jwt(db, token)
    assert e


def test_fail_to_decode_expired_token_one_hour_ago(db: Session):
    value = random_lower_string()
    sub = {"key": value}
    token = encode_sub_exp_jwt(sub, exp_delta_hours=-1)
    with raises(Exception) as e:
        assert decode_sub_jwt(db, token)
    assert e


def test_fail_to_decode_denied_token(db: Session):
    value = random_lower_string()
    sub = {"key": value}
    token = encode_sub_exp_jwt(sub)

    denied_token_redis.set(token, "")

    with raises(Exception) as e:
        assert decode_sub_jwt(db, token)
    assert e


def test_create_access_token(db: Session):
    any_integer = random_integer()
    any_boolean = random_boolean()
    token = create_access_token(user_id=any_integer, is_admin=any_boolean)
    assert token


def test_create_refresh_token(db: Session):
    any_integer = random_integer()
    token = create_refresh_token(user_id=any_integer)
    assert token


def test_create_password_reset_token(db: Session):
    any_email = random_email()
    token = create_password_reset_token(email=any_email)
    assert token
