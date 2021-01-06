from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from app.core import s

engine = create_engine(s.DATABASE_URL,
                       connect_args=({"check_same_thread": False} if s.DEV_MODE
                                     else {}),
                       pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
