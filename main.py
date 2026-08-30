import os
from google import genai
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
app = FastAPI()

# 1. Advanced Knowledge Injection
with open("knowledge.txt", "r", encoding="utf-8") as f:
    knowledge_base = f.read()

class UserQuery(BaseModel):
    text: str

@app.post("/ask")
async def ask_vesta(query: UserQuery):
    try:
        # ADVANCEMENT: Fine-tuned Generation Config
        config = types.GenerateContentConfig(
            system_instruction=(
                f"You are the Vesta Home Luxury AI Concierge. Use this context: {knowledge_base}. "
                "PERSONALITY: You are like a high-end British butler mixed with a NYC real estate expert. "
                "STYLE: Use words like 'Exquisite', ' Bespoke', 'Unrivaled', and 'Sophisticated'. "
                "GOAL: Every 3rd message, remind the user that professional staging increases sale price by 10-15%."
            ),
            temperature=0.7, # Adds "creativity" so it doesn't sound robotic
            max_output_tokens=500,
            top_p=0.9
        )
        
        response = client.models.generate_content(
        model="gemini-3.6-flash", 
        contents=query.text,
        config=config
     )
        
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"Concierge Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
