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
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key missing.")
    
    try:
        genai.configure(api_key=api_key)
        model_name = get_model()
        
        model = genai.GenerativeModel(
            model_name,
            system_instruction="You are a helpful assistant for Alberta Prime Senior Care Agency."
        )
        
        response = model.generate_content(request.prompt)
        return {"response": response.text}
        
    except Exception as e:
        print(f"DEBUG ERROR: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Alberta Prime AI is ready."}
