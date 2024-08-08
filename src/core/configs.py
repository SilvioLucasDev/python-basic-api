from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

from typing import Any

load_dotenv()


# Configurações gerais do projeto
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = os.getenv("DB_URL")
    DBBaseModel: Any = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
