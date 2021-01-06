from typing import Any

from sqlalchemy.orm import Session

from ...schemas.rank_schema import RankRequestSchema
from ...services import rank_service
from ..utils import random_integer
from ..utils.rank_utils import (assert_schema_db_rank,
                                create_random_rank_schema,
                                create_random_rank_with_service)


def test_create_rank_service(db: Session) -> None:
    random_rank_schema = create_random_rank_schema()
    created_rank_db = rank_service.create(db, obj_in=random_rank_schema)
    assert_schema_db_rank(random_rank_schema, created_rank_db)


def test_read_rank_service(db: Session) -> None:
    created_rank_db = create_random_rank_with_service(db)
    read_rank_db = rank_service.read(db, id=created_rank_db.id)
    assert created_rank_db == read_rank_db


def test_read_many_rank_service(db: Session) -> None:
    created_rank_db = create_random_rank_with_service(db)
    read_list_rank_db = rank_service.read_many(db)
    assert created_rank_db in read_list_rank_db


def test_update_rank_service(db: Session) -> None:
    created_rank_db = create_random_rank_with_service(db)
    new_random_rank_schema = create_random_rank_schema()
    updated_rank_db = rank_service.update(
        db, id=created_rank_db.id, obj_in=new_random_rank_schema)

    assert_schema_db_rank(new_random_rank_schema, updated_rank_db)


def test_delete_rank_service(db: Session) -> None:
    created_rank_db = create_random_rank_with_service(db)
    rank_service.delete(db, id=created_rank_db.id)
