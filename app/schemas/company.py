from typing import List, Optional
from pydantic import BaseModel
from datetime import date ,datetime
from app.schemas.user import *


class Imagedata(BaseModel):
    image:str 
    
class CompanyCreate(BaseModel):
    companyname: Optional[str] = None
    phonenumber: Optional[str] = None
    mail: Optional[str] = None
    address:Address = None
    alternativecontact: Optional[str] = None
    images_name: Optional[str] = None
    doc_name: Optional[List[str]] = None
    created_by: Optional[str] = None
    upi_id: Optional[str] = None
    order_payment_account_holder_name: Optional[str] = None


    class Config:
        orm_mode = True
        from_attributes = True     


class CompanyCreateResponse(BaseModel):
    id: Optional[int] = None
    companyid: Optional[str] = None
    companyname: Optional[str] = None
    phonenumber: Optional[str] = None
    mail: Optional[str] = None
    address:Address = None
    alternativecontact: Optional[str] = None
    images_name: Optional[str] = None
    doc_name: Optional[List[str]] = None
    created_by: Optional[str] = None
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime
    is_deleted:bool

    class Config:
        orm_mode = True
        from_attributes = True     

class Companysubscription(BaseModel):
    companyid: Optional[str] = None
    plan: Optional[str] = None
    paymentmethod: Optional[str] = None
    bankname: Optional[str] = None
    bankaccountnumber: Optional[str] = None
    accountholdername: Optional[str] = None
    amount: Optional[float] = None
    upi_id: Optional[str] = None
    paymentgateway: Optional[str] = None
    paymentstatus: Optional[str] = None
    paymentconfirmationnumber: Optional[str] = None


    class Config:
        orm_mode = True
        from_attributes = True           

class Companyapprove(BaseModel):
    companyid:str
    status_note:str
    is_approved:bool         