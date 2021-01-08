from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class FeatureModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # values = relationship(
    #     "ValuesModel", cascade="all, delete, delete-orphan")
