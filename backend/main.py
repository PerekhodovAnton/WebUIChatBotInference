import asyncio
from fastapi import FastAPI, HTTPException
from DB.postgres_intercation import DBinsert
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from LLM.model import Model
import asyncpg

app = FastAPI()

# это пока тоже тестовые данные, т.к. сервис авторизации пока не реализован
username = 'Anton'
user_type = 'admin'

# Модель указать ниже
model = Model("Qwen/Qwen2-72B-Instruct")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Глобальная переменная для пула соединений
db_pool = None

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user='postgres',
        password='sql',
        database='postgres',
        host='localhost'
    )
    print("Database connection pool created")

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()
    print("Database connection pool closed")

class InputData(BaseModel):
    text: str



@app.post("/chatbot")
async def receive_query(query: InputData):
    async with db_pool.acquire() as conn:
        try:
            query_text = query.text
            user_id = await DBinsert.user(conn, username, user_type)
            user_id, query_id = await DBinsert.query(conn, user_id, query_text)
            prediction = model.get_prediction(query_text)
            await DBinsert.response(conn, prediction[:200], query_id)
            return {"message": prediction}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
            
