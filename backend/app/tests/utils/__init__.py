import random
import string
from datetime import date, datetime

from pydantic.networks import EmailStr
from sqlalchemy.sql.sqltypes import DateTime


def is_dict_in_dict(dict_a, dict_b):
    return dict_a.items() <= dict_b.items()


def is_schema_in_model(schema, model):
    return is_dict_in_dict(schema.dict(), model_to_dict(model))


def is_dict_in_response(dict, response):
    return is_dict_in_dict(dict, response.json())


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


def random_email() -> EmailStr:
    return EmailStr(f"{random_lower_string()}@{random_lower_string()}.com")


def is_success_code_response(response) -> bool:
    return 200 <= response.status_code < 300


def is_error_code_response(response, detail: str = None) -> bool:

    check = 400 <= response.status_code < 500
    if check and detail:
        json = response.json()
        check = json['detail'] == detail

    return check


def has_error_detail(e, detail: str = None) -> bool:
    return e.value.detail == detail  # type: ignore
