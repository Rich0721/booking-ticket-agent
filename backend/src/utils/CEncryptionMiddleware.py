import json
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from src.core.CSettings import settings
from src.utils.CEncryptionService import CEncryptionService


class CEncryptionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.__service = CEncryptionService()

    async def dispatch(self, request: Request, call_next):
        if not settings.encryption_enabled:
            return await call_next(request)

        encrypted_header: str = request.headers.get("x-encrypted", "false").lower()
        is_encrypted: bool = encrypted_header in {"1", "true", "yes"}

        if is_encrypted and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            body_bytes: bytes = await request.body()
            if body_bytes:
                payload: dict[str, Any] = json.loads(body_bytes.decode("utf-8"))
                if "payload" in payload and isinstance(payload["payload"], str):
                    decrypted_payload: dict = self.__service.decrypt_payload(payload["payload"])
                    new_body: bytes = json.dumps(decrypted_payload, ensure_ascii=False).encode("utf-8")

                    async def receive() -> dict[str, Any]:
                        return {"type": "http.request", "body": new_body, "more_body": False}

                    request._receive = receive

        response: Response = await call_next(request)

        if is_encrypted and isinstance(response, JSONResponse):
            raw_data = b""
            async for chunk in response.body_iterator:
                raw_data += chunk

            response_dict = json.loads(raw_data.decode("utf-8"))
            encrypted_payload: str = self.__service.encrypt_payload(response_dict)
            return JSONResponse(status_code=response.status_code, content={"payload": encrypted_payload})

        return response
