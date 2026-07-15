from enum import Enum

class EUserPermission(Enum):
    """使用者權限列舉"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
