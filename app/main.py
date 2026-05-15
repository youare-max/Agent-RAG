import uvicorn
from fastapi import FastAPI
from app.api.router import router

app = FastAPI(
    title="Smart After-Sales Agent",
    description="基于大模型的智能售后 Agent API",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Smart After-Sales Agent API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
