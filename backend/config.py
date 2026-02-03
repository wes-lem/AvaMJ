"""
Variáveis de ambiente: URL do Moodle, senhas, chaves API.
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações carregadas do .env."""

    # Moodle
    MOODLE_URL: str = "https://moodle.example.com"
    MOODLE_TOKEN: str = ""

    # Banco de dados (MySQL local - porta padrão 3306)
    DATABASE_URL: str = "mysql+pymysql://user:password@127.0.0.1:3306/avamj"

    # OpenAI (Chatbot)
    OPENAI_API_KEY: str = ""

    # LTI (opcional)
    LTI_SECRET: str = ""
    LTI_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
