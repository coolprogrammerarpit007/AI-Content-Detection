from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB: str

    COPYLEAKS_EMAIL: str
    COPYLEAKS_API_KEY: str

    DATABASE_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Build DATABASE_URL dynamically if not provided
if not settings.DATABASE_URL:
    settings.DATABASE_URL = (
        f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
        f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"
    )
