from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..core import s
from ..core.session import SessionLocal
from ..main import app
from .utils import random_email

s.SEND_GRID_API_KEY = ""


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# @pytest.fixture(scope="module")
# def admin_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
#     """
#     Use hardcoded FIRST admin and password to retrieve access_token
#     """
#     return get_access_token_from_email(db=db, email=s.FIRST_ADMIN)


# @pytest.fixture(scope="module")
# def user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
#     """
#     Create or update the password of the TEST_USER user to retrieve access_token
#     """
#     random_test_user_email = random_email()
#     return get_access_token_from_email(db=db, email=random_test_user_email)
