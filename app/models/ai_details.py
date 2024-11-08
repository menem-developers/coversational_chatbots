from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.db.base import Base

class Createchatbot(Base):
    __tablename__ = "chatbot"

    id = Column(Integer, primary_key=True, index=True)
    chatbotid = Column(String, nullable=False,index=True)
    userid = Column(Integer, nullable=True, index=True)
    admin_userid = Column(Integer, nullable=True, index=True)
    aidomain = Column(String, nullable=False)
    template = Column(String, nullable=False)
    chatbotname = Column(String, nullable=False)
    ainame = Column(String, nullable=False)
    aimodel = Column(String, nullable=False)
    doc_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, default=func.now())
    is_deleted = Column(Boolean, default=False)



class Createmotorinsurance(Base):
    __tablename__ = "motorinsurance"

    id = Column(Integer, primary_key=True, index=True)
    chassisno = Column(String, nullable=False, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    seatingcapacity = Column(String, nullable=False)
    bodytype = Column(String, nullable=False)
    vehicleusage = Column(String, nullable=False)
    year = Column(String, nullable=False)
    customerid = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)


class CreateCustomer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dob = Column(DateTime, nullable=False)
    gender = Column(String, nullable=False)
    mobile = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    occupation = Column(String, nullable=False)
    licensenumber = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)    


class Test_db(Base):
    __tablename__ = "test_db"

    id = Column(Integer, primary_key=True, index=True)
    docs_string = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)    

