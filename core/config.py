from pydantic import BaseSettings

class Settings(BaseSettings):
    REPLICATE_API_TOKEN: str
    JWT_SECRET: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

print("Databse successfully running")