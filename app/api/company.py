from fastapi import APIRouter, Depends, HTTPException, Request,status, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.schemas.company import *
from app.crud.company import *
from app.db.session import get_db
from app.operations.utils import *
from app.operations.utils import *
from fastapi.security import OAuth2PasswordBearer
import uuid
from supabase import create_client, Client
from io import BytesIO
from supabase import create_client, Client
import magic

router = APIRouter()

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")
SUPABASE_URL = 'https://edqjhuymghuhvtdonxup.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVkcWpodXltZ2h1aHZ0ZG9ueHVwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE3MDgyMDUsImV4cCI6MjAzNzI4NDIwNX0.iji4tGVlHK0CWzuvY5xGk6aAUruLegBM-J_vM_f8cmI'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@router.post("/company_create/")
async def companycreate(request: Request,companydetails:CompanyCreate,company_id:Optional[str]= None, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            if company_id:
                company = company_update(db=db, companydetails=companydetails, companyid=company_id)
                call_log(logger, description='company updated', status_code=200, api=request.url.path, ip=request.client.host)
                if company is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":company,
                        "message":"Success"
                    }   
                return data
            else:
                company = company_create(db=db, companydetails=companydetails)
                call_log(logger, description='company created', status_code=200, api=request.url.path, ip=request.client.host)
                if company is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":company,
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.get("/get_company/")
def getcompany(request:Request,company_id: Optional[str] =None , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            if company_id:
                company=get_company(db=db ,company_id=company_id)
                if company.doc_name is None:
                    company.doc_name = []
                if company is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data
                call_log(logger, description='company get', status_code=200, api=request.url.path, ip=request.client.host)
                if company is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":company,
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 
    
@router.get("/get_all_company/")
def getallcompany(request:Request, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            company=get_all_company(db=db)
            allcompany=[]
            for companys in company:
                if companys.doc_name is None:
                    companys.doc_name = []
                allcompany.append(companys)
            if len(allcompany) == 0:
                data={
                    "status":False,
                    "data":[],
                    "message":"Failed"
                }   
                return data
            call_log(logger, description='company get', status_code=200, api=request.url.path, ip=request.client.host)
            data={
                    "status":True,
                    "data":allcompany,
                    "message":"Success"
                }   
            return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")    

@router.patch("/company_images_docs/")
async def company_images_docs(imagedata:Imagedata,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            images=imagedata.image
            if images.startswith("data:"):
                images = images.split(",")[1]
            file_data = base64.b64decode(images)
            mime = magic.Magic(mime=True)
            content_type = mime.from_buffer(file_data)
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            if content_type == "application/pdf":
                unique_filename = f"{uuid.uuid4().hex}_{current_time}_menem.pdf"
            else:
                unique_filename = f"{uuid.uuid4().hex}_{current_time}_menem"   
            file_bytes = BytesIO(file_data).getvalue()
            response = supabase.storage.from_("ecommerce").upload(unique_filename, file_bytes, {"content-type": content_type})
            if response.status_code != 200:
                raise Exception(f"Failed to upload file: {response.json()}")
            file_url = supabase.storage.from_("ecommerce").get_public_url(unique_filename)
            expires_in = 525960 * 60
            signed_url = supabase.storage.from_("ecommerce").create_signed_url(unique_filename, expires_in)

            if signed_url is None:
                data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                return data  

            data={
                "status":True,
                "data":signed_url,
                "message":"Success"
                }   
            return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied") 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 

@router.post("/company_subscription/")
async def companysubscription(request: Request,Companysubscriptiondetails:Companysubscription, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            if Companysubscriptiondetails:
                company = company_subscription(db=db, Companysubscriptiondetails=Companysubscriptiondetails)
                call_log(logger, description='company updated', status_code=200, api=request.url.path, ip=request.client.host)
                if company is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":company,
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 

@router.post("/company_approve/")
async def companyapprove(request: Request,companyapproveddetails:Companyapprove, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            if companyapproveddetails:
                company = company_approve(db=db, companyapproveddetails=companyapproveddetails)
                call_log(logger, description='company updated', status_code=200, api=request.url.path, ip=request.client.host)
                if company is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":company,
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 
                             

@router.delete("/delete_company/")
def deletecompany(request:Request,company_id: Optional[str] =None , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            if company_id:
                company=delete_company(db=db ,company_id=company_id)
                call_log(logger, description='company deleted', status_code=200, api=request.url.path, ip=request.client.host)
                if company is None:
                    data={
                        "status":False,
                        "data":"",
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":f"company {company_id} is deleted",
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")       