from ..models import FeaturesModel
from .base_service import BaseService

rank_service = BaseService[FeaturesModel,
                           RankRequestSchema, RankRequestSchema](FeaturesModel, FeaturesModel.id)
