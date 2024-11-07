from fastapi import APIRouter, Depends, HTTPException, Request,status, Form, File, UploadFile
from sqlalchemy.orm import Session
from app.schemas.ai_details import *
from app.crud.ai_details import *
from app.db.session import get_db
from app.operations.utils import *
from app.operations.utils import *
from fastapi.security import OAuth2PasswordBearer
import uuid
from supabase import create_client, Client
from io import BytesIO
from supabase import create_client, Client
import magic
import mimetypes
import google.generativeai as genai
import pytesseract
from PIL import Image
import fitz
from io import BytesIO

router = APIRouter()

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")
SUPABASE_URL = 'https://vkddcsmkbjkqllpuurgd.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrZGRjc21rYmprcWxscHV1cmdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1NDczOTgsImV4cCI6MjA0MjEyMzM5OH0._z3yitdxmt2BmEdYixBeGy8tLv14IluFexhQzimUCB8'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


api_key = "AIzaSyASU__5e5ZTxpi-7WIGzg2TuAzQjzppqOA"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

generation_config = {
    "temperature": 0.1
}
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]


BILL_ITEMSS = [
    "Owner name",
    "VIN/Chassis Number",
    "Make",
    "Model Number",
    "Seating Capacity",
    "Year Of Make",
    "First Registration Date",
    "Date of birth",
    "phone number",
    "address",
    "licensenumber"
]

@router.post("/create_chatbot/")
async def create_chatbot(request: Request,chatbotdetails:CreateChatbot,chatbotid:Optional[str]= None,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
            if chatbotid:
                company = chatbot_update(db=db, chatbotdetails=chatbotdetails, chatbotid=chatbotid)
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
                company = chatbot_create(db=db, chatbotdetails=chatbotdetails)
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
 
@router.get("/get_chatbot_by_userid/")
async def getchatbotbyuserid(request: Request,user_id:Optional[int] = None,admin_userid:Optional[int] = None,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
                chatbot = chatbot_get_by_user_id(db=db,user_id=user_id, admin_userid=admin_userid)
                call_log(logger, description='chatbot created', status_code=200, api=request.url.path, ip=request.client.host)
                if len(chatbot) == 0:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":chatbot,
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.get("/get_chatbot_by_chatbotid/")
async def getchatbotbychatbotid(request: Request,cahtbot_id:str,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
                chatbot = get_chatbot_by_chatbotid(db=db,cahtbot_id=cahtbot_id)
                call_log(logger, description='chatbot created', status_code=200, api=request.url.path, ip=request.client.host)
                if chatbot is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":chatbot,
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
  

@router.get("/general_ai/")
async def generalai(request: Request,generalaidetails:Creategeneralai,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        userid = id
        if userid:
                chatbot = general_ai(db=db,generalaidetails=generalaidetails)
                call_log(logger, description='chatbot created', status_code=200, api=request.url.path, ip=request.client.host)
                if chatbot is None:
                    data={
                        "status":False,
                        "data":{},
                        "message":"Failed"
                    }   
                    return data    
                data={
                        "status":True,
                        "data":chatbot,
                        "message":"Success"
                    }   
                return data
        else:
            raise HTTPException(status_code=403, detail="Permission denied")    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")  

@router.post("/create_docs/")
async def create_chatbot(
    request: Request,
    doc_name: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid = payload.get("sub")

        if userid:
            file_url = None
            content_type = mimetypes.guess_type(doc_name.filename)[0]
            print(f"Content Type: {content_type}")
            if content_type is None:
                return {"error": "Could not determine content type"}
            file_data = await doc_name.read()
            original_extension = os.path.splitext(doc_name.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{original_extension}"

            bucket = supabase.storage.from_("chatbot")
            print(content_type)
            response = bucket.upload(unique_filename, file_data, {
                'content-type': content_type
            })
            print("Upload response:", response)
            if response.status_code == 200:
                file_url = bucket.get_public_url(unique_filename)
                print("Public URL:", file_url)

            else:
                return {"error": "File upload failed", "details": response.data}

            return {"message": "Chatbot created successfully", "file_url": file_url}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.post("/create_motor_insurance/")
async def createmotor(request: Request,motordetails:createcustomer,db: Session = Depends(get_db)):
    try:
        motor = create_motor(db=db,motordetails=motordetails)
        call_log(logger, description='motorinsurance created', status_code=200, api=request.url.path, ip=request.client.host)
        if motor is None:
            data={
                "status":False,
                "data":{},
                "message":"Failed"
            }   
            return data    
        data={
                "status":True,
                "data":motor,
                "message":"Success"
            }   
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")  
    
def pdf_to_pil(pdf_bytes: bytes) -> Image.Image:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pixmap = page.get_pixmap(matrix=mat)
        img = Image.open(BytesIO(pixmap.tobytes()))
        images.append(img)

    total_height = sum(img.size[1] for img in images)
    max_width = max(img.size[0] for img in images)
    combined_img = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for img in images:
        combined_img.paste(img, (0, y_offset))
        y_offset += img.size[1]
        
    os.makedirs('save_folder', exist_ok=True)
    
    save_path = os.path.join('save_folder', "stitched_image.jpg")
    combined_img.save(save_path, quality=100)

    doc.close()
    return combined_img

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

def extract_text_from_image(image) -> list:
    text = pytesseract.image_to_string(image)
    text_list = text.splitlines()
    return text_list

@router.post("/parse_user_vehicle_info/")
async def parse_user_vehicle_info(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        pdf_bytes = await file.read()
        pil_images = pdf_to_pil(pdf_bytes)
        image = pil_images
    else:
        image = Image.open(file.file)

    text_list = extract_text_from_image(image)
    # print(text_list)
    response = model.generate_content([f"""
    Extract and verify user and vehicle information from the provided document.
    The text extracted via OCR is: {text_list}
    Please extract and verify the following information:
    {BILL_ITEMSS}
    For Seating capacity, it can also contain numerical characters for example, 01 or 1 all are valid seating capacity. 
    Provide the response as a JSON object with these fields.
    If any information is missing or cannot be verified, set the value to null.
    example:
    Customs Clearance Number:null
    Interpol Number:123
    """, image], safety_settings=safety_settings, generation_config=generation_config)

    response_text = response.text
    start_index = response_text.find('{')
    end_index = response_text.rfind('}') + 1
    user_vehicle_info = json.loads(response_text[start_index:end_index])
    return user_vehicle_info
