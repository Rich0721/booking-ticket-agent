import os


class CSettings:
    def __init__(self) -> None:
        self.app_name: str = os.getenv("APP_NAME", "Booking Ticket Backend")
        self.api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
        self.db_driver: str = os.getenv("DB_DRIVER", "postgresql+psycopg2")
        self.db_host: str = os.getenv("DB_HOST", "localhost")
        self.db_port: int = int(os.getenv("DB_PORT", "5432"))
        self.db_database: str = os.getenv("DB_DATABASE", "booking_ticket")
        self.db_user: str = os.getenv("DB_USER", "postgres")
        self.db_password: str = os.getenv("DB_PASSWORD", "postgres")
        self.db_sqlite_path: str = os.getenv("DB_SQLITE_PATH", "./booking_ticket.db")
        self.rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
        self.encryption_enabled: bool = self.__get_bool_env("ENCRYPTION_ENABLED", False)
        self.encryption_key: str = os.getenv(
            "ENCRYPTION_KEY",
            "9A5vb6vQwQK0vNysGEKMluSleqrs9jwELyhl725LLJo=",
        )

    def __get_bool_env(self, key: str, default: bool) -> bool:
        value: str | None = os.getenv(key)
        if value is None:
            return default

        return value.strip().lower() in {"1", "true", "yes", "on"}


settings = CSettings()
