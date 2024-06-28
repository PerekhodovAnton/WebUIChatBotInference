# WebUI Inference for LLM from HF Gradio API or local llama.cpp (FastAPI + React + Postgres)


![webui](https://github.com/PerekhodovAnton/WebUIChatBotInference/assets/145850725/a0984bae-7aa3-40c6-9c92-5bf9567c2b82)

Look at https://huggingface.co/spaces and open one you like\
Almost every space is made with Gradio, so it is 'use api' usually at the bottom of the page\
Add your gradio api to LLM/gradio_api_model.py. Default: Qwen/Qwen2-72B-Instruct\
If you want to use llama.cpp gguf model -> download it to LLM/cache and specify path in main.py\
Postgres DB to collect all queries, responses and users if it is a need

### To dowloand test llm for llama.cpp :
Move to /backend and in command line:
```bash
bash donwload.sh
```

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
npm install
npm run dev
```
# TODO
1. Authorization 
2. Check for query validity (column already in DB)
3. Switch to on off DB and between gradio or llama.cpp
4. Simple launch in one script (like .sh)
