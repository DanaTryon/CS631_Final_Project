# app/core/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env (dev/prod)
load_dotenv()

class Settings:
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"

    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "cs631_db")

    TEST_DB_USER: str = os.getenv("TEST_DB_USER", DB_USER)
    TEST_DB_PASSWORD: str = os.getenv("TEST_DB_PASSWORD", DB_PASSWORD)
    TEST_DB_HOST: str = os.getenv("TEST_DB_HOST", DB_HOST)
    TEST_DB_PORT: str = os.getenv("TEST_DB_PORT", DB_PORT)
    TEST_DB_NAME: str = os.getenv("TEST_DB_NAME", f"{DB_NAME}_test")

    @property
    def database_url(self) -> str:
        if self.TESTING:
            return (
                f"mysql+pymysql://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}"
                f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
            )
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()