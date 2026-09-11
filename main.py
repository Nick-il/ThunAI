from fastapi import FastAPI
from pydantic import BaseModel

from rag import agent


app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():

    return {
        "message": "ThunAI API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

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