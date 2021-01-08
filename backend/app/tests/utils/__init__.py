import random
import string
from datetime import date, datetime

from sqlalchemy.sql.sqltypes import DateTime


def assert_success_and_get_dict(response):
    assert is_success_code(response)
    return response.json()


def is_schema_in_model(schema, model):
    return schema.dict().items() <= model_to_dict(model).items()


def model_to_dict(obj):
    d = {}
    for column in obj.__table__.columns:
        if len(column.foreign_keys) > 0:
            # Skip foreign keys
            continue
        if issubclass(type(column.type), DateTime):
            d[column.name] = datetime.isoformat(getattr(obj, column.name))
        else:
            d[column.name] = getattr(obj, column.name)

    return d


def random_lower_string() -> str:
    # type: ignore
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_integer(min: int = 1, max: int = 100) -> int:
    return random.randint(min, max)


def random_boolean() -> bool:
    return random.choice([True, False])


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def is_success_code(response) -> bool:
    return 200 <= response.status_code < 300


def is_http_error(response, detail: str = None) -> bool:

    check = 400 <= response.status_code < 500
    if check and detail:
        json = response.json()
        check = json['detail'] == detail

    return check


def has_error_detail(e, detail: str = None) -> bool:
    return e.value.detail == detail  # type: ignore
