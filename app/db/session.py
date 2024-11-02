from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from dotenv import load_dotenv
import os

load_dotenv('.env')

SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

