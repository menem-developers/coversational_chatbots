from typing import List, Optional
from pydantic import BaseModel
from datetime import date ,datetime


class CreateChatbot(BaseModel):
    userid:Optional[int] = None
    admin_userid:Optional[int] = None
    aidomain:str
    template:str
    chatbotname:str
    ainame:str
    aimodel:str  
    doc_name:str  
    
        
class CreateuserResponse(BaseModel):
    id:int
    chatbotid:str
    userid:Optional[int] = None
    admin_userid:Optional[int] = None
    aidomain:str
    template:str
    chatbotname:str
    ainame:str
    aimodel:str  
    doc_name: Optional[str] = None
    created_by: Optional[str] = None
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime
    is_deleted:bool 
    class Config:
        orm_mode = True
        from_attributes = True


class Creategeneralai(BaseModel):
    chatbotid:str
    template:str
    

class createmotorinsurance(BaseModel):
    chassisno:str
    make:str
    model:str
    seatingcapacity:str
    bodytype:str
    vehicleusage:str
    year:str

class motorinsuranceresponse(BaseModel):
    id:int
    chassisno:str
    make:str
    model:str
    seatingcapacity:str
    bodytype:str
    vehicleusage:str
    year:str
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime
    is_deleted:bool 
    customerid:int

    class Config:
        orm_mode = True
        from_attributes = True 

class createcustomer(BaseModel):
    name:str
    dob:date
    gender:str
    mobile:str
    address:str
    occupation:str
    licensenumber:str 
    product:createmotorinsurance   

class createcustomerresponse(BaseModel):
    name:str
    dob:date
    gender:str
    mobile:str
    address:str
    occupation:str
    licensenumber:str
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime
    is_deleted:bool 
    class Config:
        orm_mode = True
        from_attributes = True 

