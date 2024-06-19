# WebUI Inference for any model from HF Gradio API (FastAPI + React + Postgres)


![webui](https://github.com/PerekhodovAnton/WebUIChatBotInference/assets/145850725/a0984bae-7aa3-40c6-9c92-5bf9567c2b82)

Look at https://huggingface.co/spaces and open one you like \
Almost every space is made with Gradio, so it is 'use api' usually at the bottom of page \
Add your model inference to LLM/model.py so it returns predictions. Default: Qwen2-72B-Instruct \
It is Postgres to collect all queries, responses and users if it is a need \

### To run Postgres (docker):
Move to /backend/DB and in command line:
```bash
docker-compose up -d
```
### To run backend (FastAPI):
Move to /backend and in command line:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
### To run WebUI (React): 
Move to /frontend
```bash
npm run dev
```
# TODO
1. Authorization (if needed)
2. Check for query validity (column already in DB) (if needed)
3. Upgrade model insertion
