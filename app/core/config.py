from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn
from pathlib import Path


ROOT = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    # Postgresql
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str
    DB_ECHO: bool = False

    # Redis
    REDIS_USERNAME: str = "default"
    REDIS_PASSWORD: str = ""
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: str = "0"

    MEDIA_ROOT: Path = ROOT / Path("media")
    MEDIA_URL: str = "http://localhost:8000/media/"

    # S3
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_ENDPOINT: str = ""
    S3_BUCKET: str = ""
    S3_REGION: str = ""

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME
        )

    @property
    def redis_url(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USERNAME,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=self.REDIS_DB
        )

settings = Settings()
