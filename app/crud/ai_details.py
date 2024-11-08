from sqlalchemy.orm import Session
from app.schemas.ai_details import *
from app.models.ai_details import *
from app.operations.utils import *
from datetime import datetime
from app.models.user import *
from app.models.user import *
from app.models.company import *
from app.schemas.company import *
from fastapi.encoders import jsonable_encoder
from datetime import datetime, time
from dateutil.relativedelta import relativedelta


def chatbot_create(db: Session, chatbotdetails: CreateChatbot):
    db_chatbot = db.query(Createchatbot).all()
    random_prefix = ''.join(random.choices(string.ascii_uppercase, k=10))
    chatbotid_suffixes = [
        int(chatbot.chatbotid[-3:]) for chatbot in db_chatbot 
        if chatbot.chatbotid and chatbot.chatbotid[-3:].isdigit()
    ]

    if chatbotid_suffixes:
        max_suffix = max(chatbotid_suffixes)
        new_suffix = max_suffix + 1
    else:
        new_suffix = 1
    new_id = f"{random_prefix}{str(new_suffix).zfill(3)}"

    db_chatbotid = Createchatbot(**chatbotdetails.dict())
    db_chatbotid.chatbotid = new_id
    db.add(db_chatbotid)
    db.commit()
    db.refresh(db_chatbotid)
    
    return db_chatbotid


def create_motor(db: Session, motordetails: createcustomer):
    # Extract product details as a dictionary
    product = motordetails.product.dict()  # Convert product to a dictionary if it's a Pydantic model

    # Remove product from motordetails to create a customer object
    db_customer = CreateCustomer(**motordetails.dict(exclude={"product"}))
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    # Assign customer ID to the product dictionary
    product["customerid"] = db_customer.id

    # Create motor insurance object with updated product dictionary
    db_motorinsurance = Createmotorinsurance(**product)
    db.add(db_motorinsurance)
    db.commit()
    db.refresh(db_motorinsurance)

    return db_motorinsurance

def chatbot_update(db:Session,chatbotdetails:CreateChatbot,chatbotid:str):
    db_chatbot = db.query(Createchatbot).filter(Createchatbot.chatbotid == chatbotid,Createchatbot.is_deleted == False).first()
    if db_chatbot:
        db_chatbot.aidomain  = chatbotdetails.aidomain
        db_chatbot.aimodel  = chatbotdetails.aimodel
        db_chatbot.ainame  = chatbotdetails.ainame
        db_chatbot.chatbotname  = chatbotdetails.chatbotname
        db_chatbot.doc_name  = chatbotdetails.doc_name
        db_chatbot.template  = chatbotdetails.template
        db.commit()
        db.refresh(db_chatbot)
        return db_chatbot

def chatbot_get_by_user_id(db:Session,user_id:int,admin_userid:int):
    if admin_userid:
        db_chatbot = db.query(Createchatbot).filter(Createchatbot.admin_userid == admin_userid,Createchatbot.is_deleted == False).all()  
    else:
        db_chatbot = db.query(Createchatbot).filter(Createchatbot.userid == user_id,Createchatbot.is_deleted == False).all() 
        print(db_chatbot) 
    return db_chatbot


def get_chatbot_by_chatbotid(db:Session,cahtbot_id:str):
    db_chatbot = db.query(Createchatbot).filter(Createchatbot.chatbotid == cahtbot_id,Createchatbot.is_deleted == False).first()
    return db_chatbot

def support(db:Session):
    db_chatbot = db.query(Test_db).filter(Test_db.id == 2,Test_db.is_deleted == False).first()
    return db_chatbot


def store(db:Session,text_list:str):
    db_store = Test_db(docs_string=text_list)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store