from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class DummyModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
