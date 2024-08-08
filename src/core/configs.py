from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


# Configurações gerais do projeto
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = os.getenv("DB_URL")

    class Config:
        case_sensitive = True


settings = Settings()
