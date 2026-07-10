import base64
import json

from cryptography.fernet import Fernet

from src.core.CSettings import settings


class CEncryptionService:
    def __init__(self) -> None:
        self.__fernet = Fernet(settings.encryption_key.encode("utf-8"))

    def encrypt_payload(self, payload: dict) -> str:
        raw_text: str = json.dumps(payload, ensure_ascii=False)
        encrypted: bytes = self.__fernet.encrypt(raw_text.encode("utf-8"))
        return base64.urlsafe_b64encode(encrypted).decode("utf-8")

    def decrypt_payload(self, payload: str) -> dict:
        decoded: bytes = base64.urlsafe_b64decode(payload.encode("utf-8"))
        raw_text: str = self.__fernet.decrypt(decoded).decode("utf-8")
        return json.loads(raw_text)
