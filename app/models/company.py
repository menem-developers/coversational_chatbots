from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Date, ForeignKey,JSON,LargeBinary
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    companyid = Column(String,nullable=True)
    companyname = Column(String,nullable=True)
    phonenumber = Column(String,nullable=True)
    mail = Column(String,nullable=True)
    address = Column(JSON,nullable=True)
    alternativecontact = Column(String,nullable=True)
    images_name = Column(String,nullable=True)
    doc_name = Column(JSON,nullable=True)
    paymentmethod  = Column(String,index=True,nullable=True)
    bankname  = Column(String,index=True,nullable=True)
    bankaccountnumber  = Column(String,index=True,nullable=True)
    accountholdername  = Column(String,index=True,nullable=True)
    upi_id  = Column(String,index=True,nullable=True)
    order_payment_account_holder_name = Column(String,index=True,nullable=True)
    amount  = Column(String,index=True,nullable=True)
    paymentgateway  = Column(String,index=True,nullable=True)
    paymentstatus  = Column(String,index=True,nullable=True)
    paymentconfirmationnumber  = Column(String,index=True,nullable=True)
    subscriptionvalidity = Column(DateTime,nullable=True)
    status_note = Column(String,index=True,nullable=True)
    plan =  Column(String,index=True,nullable=True)
    created_by = Column(String,nullable=True)
    created_at = Column(DateTime, nullable=True,default=func.now())
    updated_at = Column(DateTime, nullable=True,default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True,default=func.now())
    is_subscription = Column(Boolean, nullable=True, default=False)
    is_approved = Column(Boolean, nullable=True, default=False)
    is_deleted = Column(Boolean, nullable=True, default=False)