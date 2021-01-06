import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class UserModel(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    last_auth_change = Column(
        DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # domains = relationship(
    #     "DomainModel", cascade="all, delete, delete-orphan")
    # keywords = relationship(
    #     "KeywordModel", cascade="all, delete, delete-orphan")
