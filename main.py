from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import Base, engine, get_user_request, add_request
from gemini_client import get_answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,   
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/request")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    return {"data": get_user_request(ip_address=user_ip_address)}


@app.post("/request")
def send_prompt(request: Request, data: PromptRequest):
    user_ip_address = request.client.host
    answer = get_answer(data.prompt)

    add_request(
        ip_address=user_ip_address,
        prompt=data.prompt,
        response=answer
    )

    return {"answer": answer}