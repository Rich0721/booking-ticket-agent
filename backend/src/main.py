from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.api.booking import router as booking_router
from src.core.CSettings import settings
from src.database.CBase import CBase
from src.database.CDatabase import engine
from src.database import init_models  # noqa: F401
from src.utils.CEncryptionMiddleware import CEncryptionMiddleware
from src.utils.CRateLimitMiddleware import CRateLimitMiddleware


app = FastAPI(title=settings.app_name)
app.add_middleware(CRateLimitMiddleware)
app.add_middleware(CEncryptionMiddleware)
app.include_router(booking_router, prefix=settings.api_prefix)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"info": {"message": exc.detail}})


@app.on_event("startup")
def on_startup() -> None:
    CBase.metadata.create_all(bind=engine)


@app.get("/health")
def health_check() -> dict:
    return {"info": {"message": "ok"}}
