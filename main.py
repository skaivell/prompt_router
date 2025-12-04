from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from fastapi import Body, Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from database.crud import add_request_data, get_user_requests
from gemini_client import get_answer_from_gemini
from database.models import Base
from database.db import engine, new_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    print("Все таблицы созданы.")
    yield

app = FastAPI(
    title="Prompt_Router",
    lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


@app.get("/requests")
async def get_my_requests(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request
    ):
    user_ip_address = request.client.host
    user_requests = await get_user_requests(ip_address=user_ip_address, session=session)
    return user_requests

@app.post("/requests")
async def send_prompt(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    prompt: str = Body(embed=True)
    ):
    user_ip_address = request.client.host
    answer = await get_answer_from_gemini(prompt)
    
    await add_request_data(
        ip_address=user_ip_address,
        prompt=prompt,
        response=answer,
        session=session
    )
    return {"data": answer}