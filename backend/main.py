from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import BookingTicketController, SelectionController
import os

app = FastAPI()

origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")

# 將字串轉為串列 (List)
origins = [origin.strip() for origin in origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 註冊路由
app.include_router(BookingTicketController.router)
app.include_router(SelectionController.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
