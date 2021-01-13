from app.core import s
from app.models.feature_model import FeatureModel
from app.models.value_model import ValueModel
from app.schemas.feature_schema import FeatureCreateSchema
from app.schemas.value_schema import ValueCreateSchema
from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..models.base_model import BaseModel
from ..schemas.user_schema import UserCreateSchemaAdmin
from ..services import feature_service, user_service, value_service
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

    initial_features_and_values = [
        {"feature": "Raça", "values":  ["Humano", "Elfo", "Alien"]},
        {"feature": "Identidade de gênero", "values": [
            "Feminino", "Masculino", "Outros"]},
        {"feature": "Ação", "values": ["Correndo", "Dormindo", "Estudando"]},
        {"feature": "Como", "values": ["Feliz", "Cansado", "Zangado"]},
    ]

    for initial_feature in initial_features_and_values:
        feature_models = feature_service.read_many(db, criteria=(
            FeatureModel.name == initial_feature["feature"]))
        if feature_models:
            feature_id = feature_models[0].id
        else:
            feature_model = feature_service.create(
                db, obj_in=FeatureCreateSchema(name=initial_feature["feature"]))
            feature_id = feature_model.id

        for value in initial_feature["values"]:
            value_models = value_service.read_many(db, criteria=(
                and_(ValueModel.feature_id == feature_id, ValueModel.value == value)))
            if not value_models:
                value_model = value_service.create(
                    db, obj_in=ValueCreateSchema(value=value, feature_id=feature_id))
