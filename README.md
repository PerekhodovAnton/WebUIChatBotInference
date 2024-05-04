# WebUI Inference for any model (FastAPI + React + Postgres)


Add your model inference to LLM/model.py so it returns predictions \
It is Postgres to collect all queries, responses and users if it is a need \
Authorization will be soon...
### To run Postgres (docker):
Move to backend/DB and in command line:
```bash
docker-compose up -d
```
### To run backend (FastAPI):
Move to /backend and in command line:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
### To run WebUI (React): 
```bash
npm run dev
```