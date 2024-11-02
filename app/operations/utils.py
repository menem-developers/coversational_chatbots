import logging as custom_logging
from app.db.session import SessionLocal
from app.models.logs import *
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from dotenv import load_dotenv
import os
import hashlib
import base64
import os,random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string,requests
import json
import io
import base64
# load_dotenv('.env')

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

NOTIFICATION_URL = os.environ.get('NOTIFICATION_URL')
NOTIFICATION_KEY = os.environ.get('NOTIFICATION_KEY')

class LogDBHandler(custom_logging.Handler):
    '''
    Customized logging handler that puts logs to the database.
    '''
    def __init__(self):
        custom_logging.Handler.__init__(self)
        self.db_tbl_log = 'lms_log'

    def emit(self, record):
        if record.name == 'uvicorn.error':
            return None

        log_list = record.msg.split(',')
        log_instance = SanlamLog()
        for key_value in log_list:
            key, value = key_value.split(':', 1)
            if not value:
                value = None
            setattr(log_instance, key, value)
        log_instance.module = record.name        
        db = SessionLocal()
        db.add(log_instance)
        db.commit()
        db.close()

def call_log(logger, description='', ip='', user_id='', status_code=200, api=''):
    logger.info('description:{description},ip:{ip},user_id:{user_id},status_code:{status_code},api:{api}'.format(
        description = description,
        ip = ip,
        user_id = user_id,
        status_code = status_code,
        api = api
    ))


def get_logger(module_name):
    handler_instance = LogDBHandler()
    custom_logging.getLogger('').addHandler(handler_instance)
    custom_logging.basicConfig(filename='log.txt')
    logger = custom_logging.getLogger(module_name)
    logger.setLevel('DEBUG')
    return logger


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire })
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire })
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

FIXED_SALT = b'menem@123'
def hash_password(password: str):
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), FIXED_SALT, 100000)
    return base64.b64encode(FIXED_SALT + key).decode('utf-8')

def verify_password(stored_password: str, provided_password: str):
    salt_and_key = base64.b64decode(stored_password.encode('utf-8'))
    salt, stored_key = salt_and_key[:len(FIXED_SALT)], salt_and_key[len(FIXED_SALT):]
    key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return key == stored_key

def generate_otp():
    # otp = ''.join(random.choices(string.ascii_uppercase, k=6))
    otp = random.randint(100000, 999999)
    expires_at = datetime.now() + timedelta(minutes=5)
    expires_at_str = expires_at.strftime("%Y-%m-%d %H:%M:%S")
    return str(otp), expires_at_str


def is_otp_expired(expires_at_str):
    expires_at = datetime.strptime(expires_at_str, "%Y-%m-%d %H:%M:%S")
    return datetime.now() < expires_at

def send_verification_email(username, to, subject, otp):
    try:
        print(username)
        text = 'Hi {},\nThank you for being associated with our MeNeM Social Networking Service. Use the following OTP to complete your account procedures.\n{}\nOTP is valid for 5 minutes, Our executives never ask you about one time password. In case you have not logged in to your account. please contact our customer service . You can also write an email at support@menem.in\nRegards,\nMeNeM'.format(username, otp)
        server = smtplib.SMTP(os.environ.get('SMTP_SERVER'), os.environ.get('SMTP_SERVER_NUM'))
        server.connect(os.environ.get('SMTP_SERVER'), os.environ.get('SMTP_SERVER_NUM'))
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(os.environ.get('SMTP_FROM'), os.environ.get('SMTP_APP_PASSWORD'))
        msg = 'Subject: {}\n\n{}'.format(subject, text)
        server.sendmail(os.environ.get('SMTP_FROM'), to, msg)
        server.quit()
        return { 'status': True }
    except Exception as e:
            print(str(e))
            return { 'status': False, 'error': {'message': 'Sending Mail Failed'}}
    
def send_notification(mobile_token, Title, body_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTIFICATION_KEY}, key={NOTIFICATION_KEY}"
    }

    payload = {
        "message": {
            "token": mobile_token,
            "notification": {
                "title": Title,
                "body": body_message
            }
        }
    }

    response = requests.post(NOTIFICATION_URL, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.json()) 
    return response

# def send_mobile_otp(username, to, subject, otp):
#     try:
#         text = 'Hi {},\nThank you for being associated with our MeNeM Social Networking Service. Use the following OTP to complete your account procedures.\n{}\nOTP is valid for 10 minutes, Our executives never ask you about one time password. In case you have not logged in to your account. please contact our customer service . You can also write an email at support@menem.in\nRegards,\nMeNeM'.format(username, otp)
#         server = smtplib.SMTP(os.environ.get('SMTP_SERVER'), os.environ.get('SMTP_SERVER_NUM'))
#         server.connect(os.environ.get('SMTP_SERVER'), os.environ.get('SMTP_SERVER_NUM'))
#         server.ehlo()
#         server.starttls()
#         server.ehlo()
#         server.login(os.environ.get('SMTP_FROM'), os.environ.get('SMTP_APP_PASSWORD'))
#         msg = 'Subject: {}\n\n{}'.format(subject, text)
#         server.sendmail(os.environ.get('SMTP_FROM'), to, msg)
#         server.quit()
#         return { 'status': True }
#     except Exception as e:
#             print(str(e))
#             return { 'status': False, 'error': {'message': 'Sending Mail Failed'}}