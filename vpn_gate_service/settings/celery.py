import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    CELERY_RESULT_BACKEND: str
    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")
