from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ai_chatbot import router as ai_router
from app.api.company import router as company_router
from app.api.user import router as user_router
from app.api.adminuser import router as adminuser_router
from app.api.ai_details import router as aidetails_router

import os
app = FastAPI(title='Menem Message Application',description="Menem Message Application",version='1.0.0')

app.add_middleware(CORSMiddleware,allow_origins=["*"], allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
app.include_router(company_router, prefix="/api/v1/company", tags=["Company"])
app.include_router(adminuser_router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(aidetails_router, prefix="/api/v1/chatbot", tags=["Chatbot"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI"])


@app.get('/')
async def root():
    return {'status': 'alive'}

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)