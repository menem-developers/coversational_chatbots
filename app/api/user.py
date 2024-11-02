from fastapi import APIRouter, Depends, HTTPException, Request,status,Form
from sqlalchemy.orm import Session
from app.schemas.user import *
from app.crud.user import *
from app.db.session import get_db
from app.operations.utils import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from dotenv import load_dotenv
import os
from jose import jwt,JWTError

# load_dotenv('.env')

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get('REFRESH_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

router = APIRouter()

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

@router.post("/create_user/")
def createuser(request:Request, userdetails: Createuser,user_id:Optional[str] = None, db: Session = Depends(get_db)):
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
                    phonenumber=user_check(db=db,companyid=userdetails.companyid,email=userdetails.email)
                    if phonenumber is not None:
                        raise HTTPException(status_code=400,detail='User already registered')
                user= create_user(db=db, userdetails=userdetails)
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
    
@router.post("/guest_token/")
def guesttoken(request:Request,email:str,password:str ,db: Session = Depends(get_db)):
    try:
        verify=user_login(db=db,email=email,password=password)
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
                "message":"Failed"
            }   
            return data    
        data={
                "status":True,
                "access_token":access_token,
                "refresh_token":refresh_token,
                "message":"Success"
            }   
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
      
    
@router.post("/login/")
def userlogin(request:Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        email = form_data.username.lower()
        password = form_data.password
        verify=user_login(db=db,email=email,password=password)
        if verify is None:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": str(verify.id)}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": str(verify.id)}, expires_delta=refresh_token_expires)
        call_log(logger, description='Login Successful', status_code=200, api=request.url.path, ip=request.client.host)
        if access_token and refresh_token is None:
            data={
                "status":False,
                "message":"Failed"
            }   
            return data    
        data={
                "status":True,
                "access_token":access_token,
                "refresh_token":refresh_token,
                "message":"Success"
            }   
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")      
    
@router.get("/get_user/")
def getuser(request:Request, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if  userid:
            user=get_user(db=db ,user_id=userid)
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}") 

@router.get("/get_user_by_id/")
def getuserbyid(request:Request, user_id:int,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if  userid:
            user=get_user(db=db ,user_id=user_id)
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")     
    
@router.get("/get_all_user/")
def getalluser(request:Request,companyid:str , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if companyid and userid:
            user=get_all_user(db=db ,companyid=companyid)
            call_log(logger, description='User created', status_code=200, api=request.url.path, ip=request.client.host)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")  

             
@router.put("/reset_or_change_password/")
def resetpassword(request:Request,user_id: int, new_password:str,old_password:Optional[str] = None, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        if new_password:
            new_password = hash_password(password=new_password)
            print(old_password)
            product = reset_password(db=db ,user_id=user_id,old_password=old_password,new_password=new_password)
            if product is None:
                raise HTTPException(status_code=500, detail="Product not found") 
            call_log(logger, description='Product created', status_code=200, api=request.url.path, ip=request.client.host)
            return "Password changed"
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/google_auth_create/")
def googleauthcreate(request:Request, userdetails: Gsignin, db: Session = Depends(get_db)):
    try:
        if userdetails:
                if userdetails.email:
                    user=user_check_auth(db=db,userdetails=userdetails)
                    if user is None:
                        user= auth_create_user(db=db, userdetails=userdetails)
                call_log(logger, description='Auth created', status_code=400, api=request.url.path, ip=request.client.host)
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
                refresh_token = create_refresh_token(data={"sub": str(user.id)}, expires_delta=refresh_token_expires)
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
                        "access_token":access_token,
                        "refresh_token":refresh_token,
                        "message":"Success"
                    }   
                return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")  

@router.patch("/send_otp/")
def otpsend(request:Request,companyid: str,mobile:Optional[str] = None,email:Optional[str] = None, db: Session = Depends(get_db)):
    try:
        # payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        # id: str = payload.get("sub")
        # user_id = id
        if mobile or email:
            otp = otp_send(db=db ,mobile=mobile,email=email,companyid=companyid)
            if otp is None:
                data={
                        "status":False,
                        "data":"User not found",
                        "message":"Failed"
                    }   
                return data    
            call_log(logger, description='OTP sent', status_code=200, api=request.url.path, ip=request.client.host)
            data={
                    "status":True,
                    "data":"OTP sent successfully",
                    "message":"Success"
                }   
            return data
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")     
    
# @router.put("/mobile_otp/")
# def mobileotpsend(request:Request,phonenumber: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
#     try:
#         if phonenumber:
#             product = mobile_otp_send(db=db ,phonenumber=phonenumber)
#             if product is None:
#                 raise HTTPException(status_code=500, detail="mobilenumber not found") 
#             call_log(logger, description='Product created', status_code=200, api=request.url.path, ip=request.client.host)
#             return "Otp Verified"
#         else:
#             return None
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")      
    
@router.get("/otp_verify/")
def otp_verify(request:Request,companyid:str,otp:str,email:Optional[str] = None ,mobile:Optional[str] =  None,mobile_token:Optional[str] = None, db: Session = Depends(get_db)):
    try:
        if otp:
            otp_verified = otpverify(db=db ,email=email,mobile=mobile,otp=otp,companyid=companyid,mobile_token=mobile_token)
            if otp_verified is None:
                data={
                "status":False,
                "data":"Wrong OTP or OTP Expire",
                "message":"Failed"
                }   
                return data   
            call_log(logger, description='OTP Verified', status_code=200, api=request.url.path, ip=request.client.host)
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": str(otp_verified.id)}, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(data={"sub": str(otp_verified.id)}, expires_delta=refresh_token_expires)
            data ={
                "id":otp_verified.id,
                "access_token":access_token,
                "refresh_token":refresh_token
            }
            if access_token and refresh_token is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
            data={
                    "status":True,
                    "data":data,
                    "message":"Success"
                }   
            return data
        else:
            data={
                "status":False,
                "data":{},
                "message":"Failed"
            }   
            return data    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/logout/")
def logut(request:Request,user_id: Optional[int] =None , db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if user_id and userid:
            user=User_logout(db=db ,user_id=user_id)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")             

