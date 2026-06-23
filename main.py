from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def check_models():
    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        return {"error": "API Key is missing in Render Environment"}
    
    genai.configure(api_key=api_key)
    try:
        # API Key ले देख्न सक्ने सबै मोडलहरूको लिस्ट तान्ने
        models = [m.name for m in genai.list_models()]
        return {
            "message": "Model Check Complete",
            "available_models": models
        }
    except Exception as e:
        return {"error": str(e)}
