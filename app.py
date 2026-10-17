
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AEROFLEX AI Chatbot")

client = OpenAI(api_key=api_key) if api_key else None

origins = [
    x.strip()
    for x in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if x.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)

@app.get("/")
def home():
    return {
        "status": "online",
        "brand": "AEROFLEX"
    }

@app.post("/chat")
def chat(data: ChatRequest):
    if not client:
        raise HTTPException(
            status_code=503,
            detail="AI API key abhi configure nahi hui."
        )

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions="""
            You are the official AI assistant for AEROFLEX,
            a clothing manufacturer in Sialkot, Pakistan.

            Help customers with OEM/ODM manufacturing,
            oversized T-shirts, hoodies, varsity jackets,
            streetwear, custom clothing and bulk orders.

            Ask about product, quantity, fabric, sizes,
            customization and delivery destination.

            Never invent prices, minimum order quantities,
            production times or shipping promises.
            Ask the AEROFLEX team to confirm unknown details.
            Reply in the customer's language.
            """,
            input=data.message
        )

        return {"reply": response.output_text}

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI reply nahi mil saka. Dobara try karein."
        )
      
