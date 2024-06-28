import asyncio
from llama_cpp import Llama
from concurrent.futures import ThreadPoolExecutor

class CPPModel:
    def __init__(self, gguf_path):
        self.model = Llama(gguf_path)
        self.executor = ThreadPoolExecutor()

    def _predict(self, text:str):
        return self.model(text)
    
    async def get_prediction(self, text:str) -> str:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(self.executor, self._predict, text)
        return result['choices'][0]['text']
