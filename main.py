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

# स्मार्ट मोडल छनोटकर्ता
def get_model():
    # प्राथमिकता क्रम: flash -> 1.5 -> pro
    priority_list = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
    
    genai.configure(api_key=os.environ.get("AI_API_KEY"))
    
    # उपलब्ध मोडलहरूको लिस्ट तान्ने
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # प्राथमिकता अनुसार मोडल छान्ने
    for model_name in priority_list:
        if any(model_name in m for m in available):
            return model_name
            
    return 'gemini-1.5-flash' # Default विकल्प

@app.post("/ask-ai")
async def get_ai_response(request: PromptRequest):
    api_key = os.environ.get("AI_API_KEY")
    genai.configure(api_key=api_key)
    
    try:
        # मोडलको नाम सिधै नलेख्नुहोस्, यो तरिकाले सिधै उपलब्ध मोडल लिन्छ
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(request.prompt)
        return {"response": response.text}
        
    except Exception as e:
        # यदि 404 आयो भने, हामी सिधै 'gemini-1.0-pro' मा स्विच गर्छौँ
        try:
            model = genai.GenerativeModel('gemini-1.0-pro')
            response = model.generate_content(request.prompt)
            return {"response": response.text}
        except Exception as e2:
            print(f"DEBUG ERROR: {str(e2)}")
            raise HTTPException(status_code=500, detail=str(e2))

@app.get("/")
async def root():
    return {"message": "Alberta Prime AI is ready."}
