import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class ValueModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    feature_id = Column(Integer, ForeignKey('feature.id'))
