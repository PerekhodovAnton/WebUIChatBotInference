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

class InputData(BaseModel):
    text: str

@app.post("/chatbot")
async def receive_query(query: InputData): 
    pool = await asyncpg.create_pool(
        user='postgres',
        password='sql',
        database='postgres',
        host='localhost'
    )

    db_pooled = DBinsert(pool) 

    try:
        query_text = query.text
        user_id = await db_pooled.user(username, user_type)
        user_id, query_id = await db_pooled.query(user_id, query_text)
        prediction = model.get_prediction(query_text)
        await db_pooled.response(prediction, query_id)
        return {"message": prediction}
    
    except Exception as e:
        print(e) 
  