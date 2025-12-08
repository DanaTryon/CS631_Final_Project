# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TESTING = os.getenv("TESTING", "false").lower() == "true"
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "cs631_db")

    @property
    def database_url(self):
        if self.TESTING:
            return "sqlite:///./ci_test.db"
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()