# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

# from .base_model import BaseModel


# class DomainModel(BaseModel):
#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey('user.id'))
#     keywords = relationship(
#         "KeywordModel", cascade="all, delete, delete-orphan")
