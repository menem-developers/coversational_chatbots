from typing import List, Optional
from pydantic import BaseModel
from datetime import date ,datetime


class Address(BaseModel):
    name:Optional[str] = None
    phonenumber:Optional[str] = None
    address_type:Optional[int] = None
    address_line1:Optional[str] = None
    address_line2:Optional[str] = None
    area:Optional[str] = None
    city:Optional[str] = None
    state:Optional[str] = None
    zipcode:Optional[str] = None

class Createaddress(BaseModel):
   companyid:str
   userid:int
   address:List[Address]
   
        
class CreateaddressResponse(BaseModel):
    id: int
    companyid:str
    userid:int
    address:List[Address]

    class Config:
        orm_mode = True
        from_attributes = True

class Createuser(BaseModel):
   companyid:str
   name:str
   email:str
   gender:Optional[str] = None
   profilepic:Optional[str] = None
   address:Optional[Address] = None
   phonenumber:Optional[str] = None
   password:Optional[str] = None
   account_active:Optional[bool] = None
   mobile_token:Optional[str] = None
   signintype:Optional[str] = None

class Gsignin(BaseModel):
    companyid:str
    name:str
    email:str
    phonenumber:Optional[str] = None
    mobile_token:Optional[str] = None
    signintype:Optional[str] = None
        
class CreateuserResponse(BaseModel):
    id: int
    name:str
    companyid:str
    email:Optional[str] = None
    phonenumber:Optional[str] = None
    mobile_token:Optional[str] = None
    gender:Optional[str] = None
    profilepic:Optional[str] = None
    address:Optional[Address] = None
    account_active:Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True