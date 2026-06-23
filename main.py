from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
import traceback

app = FastAPI()

# CORS Middleware (Frontend communication को लागि)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

# Helper function: उपलब्ध मोडलहरूबाट सही मोडल छान्ने
def get_best_model():
    models = genai.list_models()
    for m in models:
        # generateContent support गर्ने मोडल खोज्ने
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return 'gemini-1.5-flash' # यदि कुनै भेटिएन भने Default

@app.post("/ask-ai")
async def get_ai_response(request: PromptRequest):
    api_key = os.environ.get("AI_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="Server Configuration Error: API Key missing.")
    
    try:
        genai.configure(api_key=api_key)
        
        # यहाँ हामी आफै मोडलको नाम खोज्छौं
        model_name = get_best_model()
        
        model = genai.GenerativeModel(
            model_name,
            system_instruction="You are a helpful assistant for Alberta Prime Senior Care Agency."
        )
        
        response = model.generate_content(request.prompt)
        return {"response": response.text}
        
    except Exception as e:
        error_info = traceback.format_exc()
        print(f"DEBUG ERROR: {error_info}")
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Alberta Prime API is live and running!"}
