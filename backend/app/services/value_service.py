from ..models import ValueModel
from ..schemas.value_schema import ValueCreateSchema
from .base_service import BaseService

value_service = BaseService[ValueModel,
                            ValueCreateSchema, ValueCreateSchema](ValueModel, ValueModel.id)
