from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
import traceback

app = FastAPI()

# CORS Middleware (Frontend बाट आउने request को लागि)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask-ai")
async def get_ai_response(request: PromptRequest):
    # API Key चेक गर्ने
    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Server Configuration Error: AI_API_KEY is missing.")
    
    try:
        genai.configure(api_key=api_key)
        
        # मोडल initialize गर्ने
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction="You are a helpful assistant for Alberta Prime Senior Care Agency."
        )
        
        # AI बाट उत्तर प्राप्त गर्ने
        response = model.generate_content(request.prompt)
        return {"response": response.text}
        
    except Exception as e:
        # Error details लाई Render logs मा देखाउन
        error_info = traceback.format_exc()
        print(f"DEBUG ERROR: {error_info}")
        
        # Frontend लाई स्पष्ट Error सन्देश पठाउन
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")
