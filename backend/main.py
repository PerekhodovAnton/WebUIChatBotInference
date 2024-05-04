import asyncio
import asyncpg
from fastapi import FastAPI
from DB.postgres_intercation import DBinsert, connect_to_database
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time 
from LLM.model import Model


app = FastAPI()

# это пока тоже тестовые данные, т.к. сервис авторизации пока не реализован
username = 'Anton'
user_type = 'admin'

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    text: str


@app.post("/chatbot")
async def receive_query(query: InputData):
    conn = await connect_to_database(
        user='postgres',
        password='sql',
        database='postgres',
        host='localhost'
        )
    query = query.text
    user_id = await DBinsert.user(conn, username, user_type) 
    user_id, query_id = await DBinsert.query(conn, user_id, query) 
    summary = Model.model(query)
    await DBinsert.response(conn, summary, query_id)
    await conn.close()
    return {"message": summary}
