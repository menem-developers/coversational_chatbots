from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Date, ForeignKey,JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class AdminUsers(Base):
    __tablename__ = "adminuser"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    email = Column(String,index=True)
    gender = Column(String,index=True)
    phonenumber = Column(String, nullable=True,index=True)
    address = Column(JSON, nullable=True)
    companyid= Column(String, nullable=True)
    signintype= Column(String, nullable=True)
    otp = Column(Integer, nullable=True)
    mobile_token = Column(String, nullable=True)
    password = Column(String, nullable=True)
    is_superadmin = Column(Boolean, nullable=True, default=False)
    superadminrole = Column(Integer, nullable=True)
    is_admin = Column(Boolean, nullable=True, default=False)
    adminrole = Column(Integer, nullable=True)
    is_staff = Column(Boolean, nullable=True, default=True)
    staffrole = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True,default=func.now())
    updated_at = Column(DateTime, nullable=True,default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True,default=func.now())
    is_deleted = Column(Boolean, nullable=True, default=False)
    is_active = Column(Boolean, nullable=True, default=True)   