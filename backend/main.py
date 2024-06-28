import asyncpg
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from DB.postgres import DBInteractions
from LLM.gradio_api_model import GradioModel
from LLM.llamacpp_model import CPPModel
from huggingface_hub import hf_hub_download

# Test data, no authorization yet
username = 'Anton'
user_type = 'admin'

# Model initializations

# Sync gradio api model
# gradio_model = GradioModel("Qwen/Qwen2-72B-Instruct")

# Async local llama.cpp model (gguf)
cpp_model = CPPModel("LLM/cache/tinyllama-1.1b-chat-v0.3.Q5_K_M.gguf")

class InputData(BaseModel):
    text: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await asyncpg.create_pool(
        user='postgres',
        password='sql',
        database='postgres',
        host='localhost'
    )
    app.state.pool = pool
    print('pool is created')
    yield
    await pool.close()
    print('pool is closed')

app = FastAPI(lifespan=lifespan)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Gradio model sync
# @app.post("/chatbot")
# async def gradio_chatbot(query: InputData):
#     query_text = query.text
#     prediction = gradio_model.get_prediction(query_text)

#     async with app.state.pool.acquire() as conn:
#         async with conn.transaction():
#             user_id = await DBInteractions.user(conn, username, user_type)
#             query_id, user_id = await DBInteractions.query(conn, user_id, query_text)
#             await DBInteractions.response(conn, prediction, query_id)

#     return {"message": prediction}


#------------------------------------------------------------------------------------------------------------------------

# CPP model async
@app.post("/chatbot")
async def cpp_prediction(query: InputData):
    query_text = query.text
    prediction = await cpp_model.get_prediction(query_text)

    async with app.state.pool.acquire() as conn:
        async with conn.transaction():
            user_id = await DBInteractions.user(conn, username, user_type)
            query_id, user_id = await DBInteractions.query(conn, user_id, query_text)
            await DBInteractions.response(conn, prediction, query_id)

    return {"message": prediction}

