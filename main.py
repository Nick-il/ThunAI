import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag import agent

app = FastAPI()

BASE_DIR = Path(__file__).parent
FRONTEND_DIR = BASE_DIR / "frontend"

# index.html references /static/styles.css and /static/app.js,
# so the frontend folder is mounted under /static to match.
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    start = time.time()

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": request.message}
        ]
    })

    latency = round(time.time() - start, 2)

    return {
        "response": result.get("answer", ""),
        "route": result.get("route", "unknown"),
        "sources": result.get("sources", []),
        "latency_seconds": latency,
    }