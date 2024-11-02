from typing import List, Optional
from pydantic import BaseModel
from datetime import date ,datetime
from app.schemas.user import *

class Superadminlogin(BaseModel):
    email:str
    password:str

class Adminlogin(BaseModel):
    companyid:str
    email:str
    password:str

class Adminuser(BaseModel):    
    name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    phonenumber: Optional[str] = None
    address: Optional[Address] = None
    signintype: Optional[str] = None
    companyid: Optional[str] = None
    mobile_token:Optional[str] = None
    password:Optional[str] = None
    is_superadmin:Optional[bool] = None
    superadminrole:Optional[int] = None
    is_admin:Optional[bool] = None
    adminrole:Optional[int] = None
    is_staff:Optional[bool] = None
    staffrole:Optional[int] = None

class AdminuserResponse(BaseModel):    
    name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    phonenumber: Optional[str] = None
    address: Optional[Address] = None
    signintype: Optional[str] = None
    companyid: Optional[str] = None
    mobile_token:Optional[str] = None
    password:Optional[str] = None
    is_superadmin:Optional[bool] = None
    superadminrole:Optional[int] = None
    is_admin:Optional[bool] = None
    adminrole:Optional[int] = None
    is_staff:Optional[bool] = None
    staffrole:Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None