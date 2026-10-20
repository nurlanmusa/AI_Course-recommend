from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"

    model_config= SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",)

    @property

    def database_url(self):
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

@lru_cache
def get_settings():
    return Settings()