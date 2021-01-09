from datetime import datetime, timedelta
from typing import Any, Dict, Union

import app.core.error_msgs as error_msgs
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core import s
from ..services import denied_token_redis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def encode_sub_exp_jwt(
        sub: Dict[str, Any],
        exp_delta_hours: float = 1,
        secret: str = s.JWT_SECRET_KEY
) -> str:
    expire = datetime.utcnow() + timedelta(hours=exp_delta_hours)
    expire_timestamp = expire.timestamp()
    to_encode = {**sub, "exp": expire_timestamp}

    encoded = jwt.encode(
        to_encode, secret, algorithm=s.JWT_ALGORITHM)
    return encoded


def decode_sub_jwt(
        db: Session,
        token: str
) -> Dict[str, Any]:
    """
    Decode a jwt token. It fails if token is denied, invalid or expired.
    """

    try:
        if denied_token_redis.exists(token):
            raise Exception(error_msgs.DENIED_TOKEN)

        payload = jwt.decode(
            token, s.JWT_SECRET_KEY, algorithms=s.JWT_ALGORITHM
        )
        exp = payload.get("exp")

        now_timestamp = datetime.utcnow().timestamp()
        if now_timestamp > exp:  # type: ignore
            raise jwt.ExpiredSignatureError

    except jwt.ExpiredSignatureError as e:
        raise Exception(error_msgs.EXPIRED_TOKEN)

    except jwt.JWTError as e:
        raise Exception(error_msgs.INVALID_TOKEN)

    return payload  # type: ignore


def create_access_token(
        *,
        user_id: int,
        is_admin: bool,
        exp_delta_hours: float = s.ACCESS_TOKEN_EXPIRE_HOURS
) -> str:
    encoded = encode_sub_exp_jwt(
        {"user_id": user_id, "is_admin": is_admin}, exp_delta_hours)
    return encoded


def create_refresh_token(
        *,
        user_id: int,
        exp_delta_hours: float = s.REFRESH_TOKEN_EXPIRE_HOURS
) -> str:
    now = datetime.utcnow().timestamp()
    encoded = encode_sub_exp_jwt(
        {"user_id": user_id, "token_timestamp": now}, exp_delta_hours=exp_delta_hours)
    return encoded


def create_password_reset_token(
        *,
        email: str,
        exp_delta_hours: float = s.EMAIL_RESET_TOKEN_EXPIRE_HOURS
) -> str:
    encoded = encode_sub_exp_jwt({"email": email}, exp_delta_hours)
    return encoded


def create_activation_token(
        *,
        email: str,
        exp_delta_hours: float = s.EMAIL_ACTIVATION_TOKEN_EXPIRE_HOURS
) -> str:
    now = datetime.utcnow().timestamp()
    encoded = encode_sub_exp_jwt(
        {"email": email, "token_timestamp": now, 'is_active': True}, exp_delta_hours)
    return encoded
