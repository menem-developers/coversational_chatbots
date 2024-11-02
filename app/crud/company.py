from sqlalchemy.orm import Session
from app.schemas.company import *
from app.models.company import *
from app.operations.utils import *
from datetime import datetime
from app.models.user import *
from app.models.user import *
from app.models.company import *
from app.schemas.company import *
from fastapi.encoders import jsonable_encoder
from datetime import datetime, time
from dateutil.relativedelta import relativedelta

def company_create(db:Session, companydetails:CompanyCreate):
    db_company = db.query(Company).all()
    company_ids = [int(company.companyid) for company in db_company if company.companyid and company.companyid.isdigit()]
    if company_ids:
        max_id = max(company_ids)
        new_id = max_id + 1
    else:
        new_id = 1
    new_id_str = str(new_id).zfill(3)
    db_company =Company(**companydetails.dict())
    db_company.companyid = new_id_str
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company
   

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
    
def company_update(db:Session,companydetails:CompanyCreate,companyid:str):
    db_company = db.query(Company).filter(Company.companyid == companyid,Company.is_deleted == False).first()
    if db_company:
        db_company.companyname = companydetails.companyname
        db_company.address = serialize_address(companydetails.address)
        db_company.images_name = companydetails.images_name
        db_company.doc_name = companydetails.doc_name
        db_company.mail = companydetails.mail
        db_company.alternativecontact = companydetails.alternativecontact
        db_company.phonenumber = companydetails.phonenumber
        db_company.upi_id = companydetails.upi_id
        db_company.order_payment_account_holder_name = companydetails.order_payment_account_holder_name

        db.commit()
        db.refresh(db_company)

        return db_company
    else:
        return None

def company_subscription(db:Session,Companysubscriptiondetails:Companysubscription):
    db_company = db.query(Company).filter(Company.companyid == Companysubscriptiondetails.companyid,Company.is_deleted == False).first()
    if db_company:
        current_time = datetime.now()
        three_months_later = current_time + relativedelta(months=3)
        six_months_later = current_time + relativedelta(months=6)
        one_year_later = current_time + relativedelta(years=1)
        
        if Companysubscriptiondetails.plan == "Basic":
            subscriptionvalidity = three_months_later
        elif Companysubscriptiondetails.plan == "Standard":
            subscriptionvalidity = six_months_later
        elif Companysubscriptiondetails.plan == "Premium":    
            subscriptionvalidity = one_year_later
        
        db_company.plan = Companysubscriptiondetails.plan
        db_company.paymentmethod = Companysubscriptiondetails.paymentmethod
        db_company.bankname = Companysubscriptiondetails.bankname
        db_company.bankaccountnumber = Companysubscriptiondetails.bankaccountnumber
        db_company.accountholdername = Companysubscriptiondetails.accountholdername
        db_company.upi_id = Companysubscriptiondetails.upi_id
        db_company.amount= Companysubscriptiondetails.amount
        db_company.paymentgateway = Companysubscriptiondetails.paymentgateway
        db_company.paymentstatus = Companysubscriptiondetails.paymentstatus
        db_company.paymentconfirmationnumber = Companysubscriptiondetails.paymentconfirmationnumber
        db_company.subscriptionvalidity = subscriptionvalidity
        db_company.plan = Companysubscriptiondetails.plan

        db.commit()
        db.refresh(db_company)
        return db_company


def get_company(db:Session,company_id:str):
    db_company = db.query(Company).filter(Company.companyid == company_id,Company.is_deleted == False).first()
    return db_company

def get_all_company(db:Session):
    db_company = db.query(Company).filter(Company.is_deleted == False).all()
    return db_company

def company_approve(db:Session,companyapproveddetails:Companyapprove):
    db_company = db.query(Company).filter(Company.companyid == companyapproveddetails.companyid,Company.is_deleted == False).first()
    if db_company:
        db_company.is_approved = companyapproveddetails.is_approved
        db_company.status_note = companyapproveddetails.status_note
        db.commit()
        db.refresh(db_company)
    return db_company

def delete_company(db:Session,company_id:str):
    db_company = db.query(Company).filter(Company.companyid == company_id,Company.is_deleted == False).first()
    if db_company:
        db_company.is_deleted = True
        db.commit()
        db.refresh(db_company)
    return company_id