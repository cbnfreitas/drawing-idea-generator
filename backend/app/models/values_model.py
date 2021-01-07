import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class ValuesModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    # property_id = Column(Integer, ForeignKey('feature.id'))
    name = Column(String, index=True)
