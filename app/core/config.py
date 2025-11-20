from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    WATSON_API_URL: str
    WATSON_API_KEY: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    ENV: str = "local"

    @property
    def DB_URL(self):
        return (
            f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
