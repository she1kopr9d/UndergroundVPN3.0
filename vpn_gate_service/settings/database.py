import pydantic

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str = pydantic.Field(alias="POSTGRES_USER")
    DB_PASS: str = pydantic.Field(alias="POSTGRES_PASSWORD")
    DB_NAME: str = pydantic.Field(alias="POSTGRES_DB")

    @property
    def DATABASE_URL_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_psycopg(self):
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")
