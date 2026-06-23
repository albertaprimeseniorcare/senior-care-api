from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
import traceback

app = FastAPI()

# CORS Middleware (Frontend बाट आउने request लाई allow गर्ने)
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
    api_key = os.environ.get("AI_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="Server Configuration Error: API Key missing.")
    
    try:
        genai.configure(api_key=api_key)
        
        # यहाँ 'gemini-1.0-pro' प्रयोग गरिएको छ जुन सबै API Key मा स्थिर छ
        model = genai.GenerativeModel(
            'gemini-1.0-pro',
            system_instruction="You are a helpful assistant for Alberta Prime Senior Care Agency."
        )
        
        response = model.generate_content(request.prompt)
        return {"response": response.text}
        
    except Exception as e:
        error_info = traceback.format_exc()
        print(f"DEBUG ERROR: {error_info}")
        raise HTTPException(status_code=500, detail=str(e))

# Server रन भइरहेको छ कि छैन भनेर जाँच्न (Root Route)
@app.get("/")
async def root():
    return {"message": "Alberta Prime API is live and running!"}
