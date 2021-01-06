# import datetime

# from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

# from ..core.db.base_class import Base


# class KeywordModel(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     keyword = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey('user.id'))
#     domain_id = Column(Integer, ForeignKey('domain.id'))
#     last_rank = Column(Integer)
#     last_rank_date = Column(DateTime)

#     ranks = relationship("RankModel", cascade="all, delete, delete-orphan")
