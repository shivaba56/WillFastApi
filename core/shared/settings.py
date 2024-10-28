from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY", cast = str)
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 30  # minutes
    JWT_REFRESH_EXPIRATION_TIME: int = 60  # minutes


    DATABASE_NAME: str = config("DATABASE_NAME", cast = str)
    DATABASE_USER: str = config("DATABASE_USER", cast = str)
    DATABASE_PASSWORD: str = config("DATABASE_PASSWORD", cast = str)
    DATABASE_HOST: str = config("DATABASE_HOST", cast = str)
    DATABASE_PORT: int = config("DATABASE_PORT", cast = int)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    @property
    def DATABASE(self):
        return (
            f"postgres://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
    
    @property
    def TORTOISE_ORM(self) -> dict:
        return {
            "connections": {
                "default": self.DATABASE
            },
            "apps": {
                "models": {
                    "models": ["core.shared.models"],
                    "default_connection": "default",
                }
            }
        }

settings = Settings()

