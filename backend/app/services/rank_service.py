from ..models.rank_model import RankModel
from ..schemas.rank_schema import RankRequestSchema
from .base_service import BaseService

rank_service = BaseService[RankModel,
                           RankRequestSchema, RankRequestSchema](RankModel, RankModel.id)
