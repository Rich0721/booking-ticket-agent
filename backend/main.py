from fastapi import FastAPI
from src.controllers import BookingTicketController, SelectionController


app = FastAPI()

# 註冊路由
app.include_router(BookingTicketController.router)
app.include_router(SelectionController.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
