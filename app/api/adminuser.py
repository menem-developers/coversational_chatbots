from fastapi import APIRouter, Depends, HTTPException, Request,status,Form
from sqlalchemy.orm import Session
from app.schemas.adminuser import *
from app.crud.adminuser import *
from app.db.session import get_db
from app.operations.utils import *
from app.operations.utils import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from dotenv import load_dotenv
import os
from jose import jwt,JWTError
from fastapi_pagination import paginate, Params

# load_dotenv('.env')

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


router = APIRouter()

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

@router.post("/create_user/")
def createuser(request:Request, userdetails: Adminuser,user_id:Optional[str] = None, db: Session = Depends(get_db)):
    try:
        if userdetails:
            if user_id:
                user=update_user(db=db ,userdetails=userdetails,user_id=user_id)
                call_log(logger, description='User updated', status_code=200, api=request.url.path, ip=request.client.host)
                if user is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":user,
                        "message":"Success"
                    }   
                return data    
            else:    
                if userdetails.email:
                    phonenumber=admin_user_check(db=db,email=userdetails.email,companyid=userdetails.companyid)
                    if phonenumber is not None:
                        raise HTTPException(status_code=400,detail='User already registered')
                user= create_admin_user(db=db, userdetails=userdetails)
                call_log(logger, description='User Created', status_code=200, api=request.url.path, ip=request.client.host)
                if user is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":user,
                        "message":"Success"
                    }   
                return data    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 
    
@router.post("/admin_login/")
def adminlogin(request:Request,logindetails:Adminlogin, db: Session = Depends(get_db)):
    try:
        companyid = logindetails.companyid
        email = logindetails.email
        password = logindetails.password
        verify = admin_user_login(db=db,companyid=companyid,email=email,password=password)
        if verify is None:
            data={
                "status":False,
                "data":{},
                "message":"Failed"
            }   
            return data  
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": str(verify.id)}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": str(verify.id)}, expires_delta=refresh_token_expires)
        call_log(logger, description='Login Successful', status_code=200, api=request.url.path, ip=request.client.host)
        if access_token and refresh_token is None:
            data={
                "status":False,
                "data":{},
                "message":"Failed"
            }   
            return data    
        data={
                "status":True,
                "access_token":access_token,
                "refresh_token":refresh_token,
                "data":verify,
                "message":"Success"
            }   
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 

@router.post("/super_admin_login/")
def superadminlogin(request:Request,logindetails:Superadminlogin, db: Session = Depends(get_db)):
    try:
        email = logindetails.email
        password = logindetails.password
        verify=super_admin_user_login(db=db,email=email,password=password)
        if verify is None:
            data={
                "status":False,
                "data":{},
                "message":"Failed"
            }   
            return data  
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": str(verify.id)}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": str(verify.id)}, expires_delta=refresh_token_expires)
        call_log(logger, description='Login Successful', status_code=200, api=request.url.path, ip=request.client.host)
        if access_token and refresh_token is None:
            data={
                "status":False,
                "data":{},
                "message":"Failed"
            }   
            return data
        data={
                "status":True,
                "access_token":access_token,
                "refresh_token":refresh_token,
                "data":verify,
                "message":"Success"
            }   
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")              

@router.post("/get_admin_user/")
def getadminuser(request:Request,user_id: Optional[int] =None , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if user_id and userid:
            user=get_admin_user(db=db ,user_id=user_id)
            call_log(logger, description='User created', status_code=200, api=request.url.path, ip=request.client.host)
            if user is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
            data={
                    "status":True,
                    "data":user,
                    "message":"Success"
                }   
            return data    
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 

@router.post("/get_all_admin_user/")
def getalladminuser(request:Request,companyid: Optional[str] =None , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if companyid and userid:
            user=get_all_admin_user(db=db ,companyid=companyid)
            call_log(logger, description='get all admin user', status_code=200, api=request.url.path, ip=request.client.host)
            if len(user) == 0:
                    data={
                        "status":False,
                        "data":[],
                        "message":"Failed"
                    }   
                    return data    
            data={
                    "status":True,
                    "data":user,
                    "message":"Success"
                }   
            return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")                    

@router.post("/logout/")
def logut(request:Request,user_id: Optional[int] =None , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if user_id and userid:
            user=admin_logout(db=db ,user_id=user_id)
            call_log(logger, description='Logout', status_code=200, api=request.url.path, ip=request.client.host)
            if user is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
            data={
                    "status":True,
                    "data":user,
                    "message":"Success"
                }   
            return data     
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")  
    
@router.post("/delete_admin_user/")
def deletadminuser(request:Request,user_id: Optional[int] =None , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if user_id and userid:
            user=delete_admin_user(db=db ,user_id=user_id)
            call_log(logger, description='delete admin user', status_code=200, api=request.url.path, ip=request.client.host)
            if user is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
            data={
                    "status":True,
                    "data":user,
                    "message":"Success"
                }   
            return data 
        else:
            raise HTTPException(status_code=403, detail="Permission denied")   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")