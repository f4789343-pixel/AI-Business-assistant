from fastapi import FastAPI
from pydantic import BaseModel
from backend.llm import run_agent
app = FastAPI(title="AI Business Operations Assistant", version="1.0.0")


@app.get("/health")
def health_check():
   return {
        "status": "healthy",
        "message": "API is running"}

class ChatRequest(BaseModel):
   message: str

@app.post("/chat")
def chat(data: ChatRequest):
   start = time.perf_counter()
   response = run_agent(data.message)
   end = time.perf_counter()
   print(f"execution time:{end - start:.2f}")
   return {"message": response}


