from sqlalchemy.orm import Session
from app.schemas.user import *
from app.models.user import *
from app.operations.utils import *
from app.schemas.company import *
from app.models.company import *
from sqlalchemy.orm import Session
from app.schemas.adminuser import *
from app.models.adminuser import *
from app.operations.utils import *

def admin_user_check(db:Session,email,companyid):
    db_email = db.query(AdminUsers).filter(AdminUsers.email== email,AdminUsers.companyid== companyid,AdminUsers.is_deleted==False).first()
    return db_email

def create_admin_user(db:Session, userdetails:Adminuser):
    user_db =AdminUsers(**userdetails.dict())
    user_db.is_active = True
    user_db.password = hash_password(user_db.password )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

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

def update_user(db:Session,user_id:int,userdetails:Adminuser):
    user_db = db.query(AdminUsers).filter(AdminUsers.id== user_id,AdminUsers.is_deleted==False).first()
    if user_db:
        user_db.gender = userdetails.gender
        user_db.mobile_token = userdetails.mobile_token
        user_db.phonenumber = userdetails.phonenumber
        user_db.name = userdetails.name
        user_db.signintype = userdetails.signintype
        serialized_address = serialize_address(userdetails.address)
        user_db.address = serialized_address
        user_db.password = hash_password(userdetails.password )
        user_db.is_admin = userdetails.is_admin
        user_db.is_superadmin = userdetails.is_superadmin
        user_db.is_staff = userdetails.is_staff
        user_db.staffrole = userdetails.staffrole
        user_db.superadminrole = userdetails.superadminrole
        user_db.adminrole = userdetails.adminrole

        db.commit()
        db.refresh(user_db)
        return user_db
    
def super_admin_user_login(db:Session,email,password):
    user_db = db.query(AdminUsers).filter(AdminUsers.email== email,AdminUsers.is_deleted == False,AdminUsers.is_superadmin==True).first()
    if user_db:
        verify = verify_password(stored_password=user_db.password, provided_password=password)
        if verify:
            user_db.is_active = True
            db.commit()
            db.refresh(user_db)
            return user_db
        else:
            return None
        
def admin_user_login(db:Session,companyid,email,password):
    user_db = db.query(AdminUsers).filter(AdminUsers.companyid== companyid,AdminUsers.email== email,AdminUsers.is_deleted == False).first()
    if user_db:
        company = db.query(Company).filter(Company.companyid== companyid,Company.is_approved== True).first()
        if company:
            verify = verify_password(stored_password=user_db.password, provided_password=password)
            if verify:
                user_db.is_active = True
                db.commit()
                db.refresh(user_db)
                return user_db
    else:
        return None            
        
def get_admin_user(db:Session,user_id:int):
    db_product = db.query(AdminUsers).filter(AdminUsers.id == user_id,AdminUsers.is_deleted == False).first()
    return db_product

def get_all_admin_user(db:Session,companyid:str):
    db_product = db.query(AdminUsers).filter(AdminUsers.companyid== companyid,AdminUsers.is_deleted == False).all()
    return db_product

def admin_logout(db:Session ,user_id):
    user_db = db.query(AdminUsers).filter(AdminUsers.id == user_id,AdminUsers.is_deleted == False).first()
    if user_db :
        user_db.is_active = False
        db.commit()
        db.refresh(user_db)
        return user_db
    else:
        return None

def delete_admin_user(db:Session,user_id:int):
    user_db = db.query(AdminUsers).filter(AdminUsers.id == user_id,AdminUsers.is_deleted == False).first()
    if user_db :
        user_db.is_active = False
        user_db.is_deleted = True
        db.commit()
        db.refresh(user_db)
        return user_db
    else:
        return None       

