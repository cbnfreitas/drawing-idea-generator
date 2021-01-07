from ..models import FeaturesModel
from ..schemas.feature_schema import FeatureCreateSchema
from .base_service import BaseService

feature_service = BaseService[FeaturesModel,
                              FeatureCreateSchema, FeatureCreateSchema](FeaturesModel, FeaturesModel.id)
