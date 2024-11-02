from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func,Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class SanlamLog(Base):
    
    __tablename__ = 'ai_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    ip = Column(Text)
    module = Column(String)
    status_code = Column(Integer, default=200)
    description = Column(Text)
    api = Column(String)
    created_at = Column(DateTime, default=func.now())