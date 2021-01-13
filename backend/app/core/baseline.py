from app.core import s
from fastapi import Depends
from sqlalchemy.orm import Session

from ..models.base_model import BaseModel
from ..schemas.user_schema import UserCreateSchemaAdmin
from ..services import user_service
from .depends import get_db
from .session import engine


def baseline(db: Session = Depends(get_db)) -> None:
    BaseModel.metadata.create_all(bind=engine)  # type: ignore

    user = user_service.read_by_email(db, email=s.FIRST_ADMIN)
    if not user:
        user_in = UserCreateSchemaAdmin(
            email=s.FIRST_ADMIN,
            password=s.FIRST_ADMIN_PASSWORD,
            is_admin=True,
            is_active=True,
        )
        user = user_service.create(db, obj_in=user_in)

    user = user_service.read_by_email(db, email=s.FIRST_NORMAL_USER)
    if not user:
        user_in = UserCreateSchemaAdmin(
            email=s.FIRST_NORMAL_USER,
            password=s.FIRST_NORMAL_USER_PASSWORD,
            is_admin=False,
            is_active=True,
        )
        user = user_service.create(db, obj_in=user_in)


# Raça: Humano, Elfo, Alien
# Identidade de gênero: Masculino, Feminino, Outros
# Ação: Correndo, comendo, estudando
# Onde: Feliz, com medo, cansado
