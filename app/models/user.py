from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    companyid = Column(String, nullable=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phonenumber = Column(String, nullable=True)
    gender = Column(String,index=True)
    password = Column(String, nullable=False)
    profilepic = Column(String, nullable=True)
    otp = Column(String, nullable=True)
    account_active = Column(Boolean, nullable=True, default=True)
    address = Column(JSON, nullable=True)
    signintype = Column(String, nullable=False)
    mobile_token = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, nullable=True, default=False)
    is_active = Column(Boolean, nullable=True, default=True)