import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    SECRET_KEY: str

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")
