from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
    "model": "llama3-70b-8192",
    "messages": [
        {"role": "system", "content": "You are RamBot 🐏, a funny and helpful chatbot that makes witty jokes and puns."},
        {"role": "user", "content": req.message}
    ],
    "temperature": 0.8
}


    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return {"reply": f"Oops! Error: {response.status_code} - {response.text}"}

    data = response.json()
    reply = data["choices"][0]["message"]["content"].strip()
    return {"reply": reply}
