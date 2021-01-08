from ..models import FeatureModel
from ..schemas.feature_schema import FeatureCreateSchema
from .base_service import BaseService

feature_service = BaseService[FeatureModel,
                              FeatureCreateSchema, FeatureCreateSchema](FeatureModel, FeatureModel.id)
