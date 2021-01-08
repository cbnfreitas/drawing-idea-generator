from ..models import DummyModel
from ..schemas.dummy_schema import DummyCreateSchema
from .base_service import BaseService

dummy_service = BaseService[DummyModel,
                            DummyCreateSchema, DummyCreateSchema](DummyModel, DummyModel.id)
