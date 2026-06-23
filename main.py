from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# Frontend बाट आउने request लाई allow गर्ने (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask-ai")
async def get_ai_response(request: PromptRequest):
    # Render को Environment Variables बाट API Key तान्ने
    api_key = os.environ.get("AI_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key missing on server.")
    
    try:
        # Google Gemini AI setup गर्ने
        genai.configure(api_key=api_key)
        
        # System instruction सहित model initialize गर्ने
        # मोडलको नाम यसरी राखेर हेर्नुहोस्
model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    system_instruction="You are a helpful assistant for Alberta Prime Senior Care Agency."
)
        
        # AI सँग उत्तर माग्ने
        response = model.generate_content(request.prompt)
        return {"response": response.text}
        
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}") # यसले Render को Logs मा विस्तृत error देखाउँछ
        raise HTTPException(status_code=500, detail=str(e))
