from typing import List, Optional
from pydantic import BaseModel
from datetime import date ,datetime


class Createwishlist(BaseModel):
   name:str
   email:str
   phonenumber:str
   password:str
   usertype:str 
   
        
class CreatewishlistResponse(BaseModel):
    id: int
    name:str
    email:Optional[str] = None
    phonenumber:Optional[str] = None
    password:str
    usertype:str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True