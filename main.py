from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    from rag import agent

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": request.message
            }
        ]
    })

    return {
        "response": result.get(
            "answer",
            ""
        )
    }

