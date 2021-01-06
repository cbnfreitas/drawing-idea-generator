import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class RankModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    # keyword_id = Column(Integer, ForeignKey('keyword.id'))
    keyword_id = Column(Integer)
    rank = Column(Integer, index=True)
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
