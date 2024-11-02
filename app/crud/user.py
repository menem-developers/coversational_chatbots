from sqlalchemy.orm import Session
from app.schemas.user import *
from app.models.user import *
from app.operations.utils import *

def user_check(db:Session,email,companyid):
    db_email = db.query(User).filter(User.companyid== companyid,User.email== email,User.is_deleted==False).first()
    return db_email

def user_check_auth(db:Session,userdetails:Gsignin):
    db_email = db.query(User).filter(User.companyid== userdetails.companyid,User.email== userdetails.email,User.is_deleted==False).first()
    if db_email:
        db_email.is_active = True
        db_email.phonenumber = None
        db_email.mobile_token = userdetails.mobile_token
        db_email.signintype = userdetails.signintype
        db.commit()
        db.refresh(db_email)
    return db_email

def create_user(db:Session, userdetails:Createuser):
    userdetails.password = hash_password(userdetails.password)
    user_db =User(**userdetails.dict())
    user_db.is_active = True
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def auth_create_user(db:Session, userdetails:Gsignin):
    user_db =User(**userdetails.dict())
    user_db.password = hash_password("OA1234%pirat@#")
    user_db.is_active = True
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def user_login(db:Session,email,password):
    user_db = db.query(User).filter(User.email== email,User.is_deleted == False).first()
    if user_db is None:
        user_db = db.query(User).filter(User.phonenumber== email,User.is_deleted == False).first()  
    verify = verify_password(stored_password=user_db.password, provided_password=password)
    if verify:
        user_db.is_active = True
        db.commit()
        db.refresh(user_db)
        return user_db
    else:
        return None
    
def get_user(db:Session,user_id:int):
    db_user = db.query(User).filter(User.id == user_id,User.is_deleted == False).first()
    return db_user

def get_all_user(db:Session,companyid:str):
    db_user = db.query(User).filter(User.is_deleted == False).all()
    return db_user

def serialize_address(address: Createaddress) -> dict:
    return {
        "name": address.name,
        "phonenumber": address.phonenumber,
        "address_type": address.address_type,
        "address_line1": address.address_line1,
        "address_line2": address.address_line2,
        "area": address.area,
        "city": address.city,
        "state": address.state,
        "zipcode": address.zipcode
    }

def update_user(db:Session,userdetails:Createuser,user_id:int):
    db_user = db.query(User).filter(User.id == user_id,User.is_deleted == False).first()
    if db_user:
        db_user.name = userdetails.name
        db_user.mobile_token = userdetails.mobile_token
        db_user.phonenumber = userdetails.phonenumber
        db_user.signintype = userdetails.signintype
        db_user.account_active = userdetails.account_active
        db_user.address = serialize_address(userdetails.address)
        db_user.gender = userdetails.gender
        db_user.profilepic = userdetails.profilepic
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None
    
def reset_password(db:Session,user_id:int,old_password,new_password):
    user_db = db.query(User).filter(User.id == user_id,User.is_deleted == False).first()
    if old_password:
        verify = verify_password(stored_password=user_db.password, provided_password=old_password)
        if user_db and verify:
            user_db.password = new_password
            db.commit()
            db.refresh(user_db)
            return user_db
        else:
            return None
    else:    
        if user_db:
            user_db.password = new_password
            db.commit()
            db.refresh(user_db)
            return user_db
        else:
            return None    
    
def otp_send(db:Session,mobile:str,email:str,companyid:str):
    if email:
        user_db = db.query(User).filter(User.email == email,User.companyid == companyid,User.is_deleted == False).first()
        if user_db is None:

            db_product =User(companyid=companyid,email=email)
            db_product.password = hash_password("OA1234%pirat@#")
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            user_db = db.query(User).filter(User.email == db_product.email,User.companyid == companyid,User.is_deleted == False).first()
        otp,expiry=generate_otp()
        if user_db.email:
            db_otp=otp+"|"+expiry
            user_db.otp = db_otp
            db.commit()
            db.refresh(user_db)
            subject="VERIFICATION OTP"
            send_verification_email(user_db.name,user_db.email , subject, otp)
            return user_db    
            
    else:
        user_db = db.query(User).filter(User.phonenumber == mobile,User.companyid == companyid,User.is_deleted == False).first()
        if user_db is None:
            db_product =User(companyid=companyid,phonenumber=mobile)
            db_product.password = hash_password("OA1234%pirat@#")
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            user_db = db.query(User).filter(User.phonenumber == db_product.phonenumber,User.companyid == companyid,User.is_deleted == False).first()   
        return None
    
# def mobile_otp_send(db:Session,phonenumber:str):
#     user_db = db.query(Users).filter(Users.phonenumber == phonenumber,Users.is_deleted == False).first()
#     otp=generate_otp()
#     if user_db:
#         user_db.otp = otp
#         db.commit()
#         db.refresh(user_db)
#         send_mobile_otp(user_db.name, phonenumber, "OTP Verification", otp)
#         return user_db    
    
def otpverify(db:Session,otp:str,email:str,mobile:str,companyid:str,mobile_token:str):
    if email:
        user_db = db.query(User).filter(User.email == email,User.companyid == companyid,User.is_deleted == False).first()
        if user_db:
            db_otp=user_db.otp
            db_otp, expires_at_str = db_otp.split('|')
            status = is_otp_expired(expires_at_str)
            if db_otp == otp:
                if status:
                    user_db.mobile_token = mobile_token
                    user_db.is_active = True
                    db.commit()
                    db.refresh(user_db)
                    return user_db   
    else:
        return None

def User_logout(db:Session ,user_id):
    user_db = db.query(User).filter(User.id == user_id,User.is_deleted == False).first()
    if user_db :
        user_db.is_active = False
        db.commit()
        db.refresh(user_db)
        return user_db
    else:
        return None