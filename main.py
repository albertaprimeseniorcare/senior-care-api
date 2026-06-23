from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "Alberta Prime AI is ready."}

@app.post("/ask-ai")
async def get_ai_response(request: PromptRequest):
    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key missing.")
    
    try:
        genai.configure(api_key=api_key)
        
        # यहाँ हामीले तपाईंको उपलब्ध लिस्टबाट ठ्याक्कै मिल्ने नाम राखेका छौँ
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        response = model.generate_content(request.prompt)
        return {"response": response.text}
        
    except Exception as e:
        print(f"DEBUG ERROR: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
