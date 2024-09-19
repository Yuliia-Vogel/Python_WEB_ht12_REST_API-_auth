# Налаштування JWT
from pydantic import BaseSettings

class Settings(BaseSettings):
    authjwt_secret_key: str = "supersecretkey"

settings = Settings()
