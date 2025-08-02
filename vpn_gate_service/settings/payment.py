
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    CRYPTO_ADDRESS: str
    CRYPTO_WEB: str

    HANDLE_ADDRESS: str
    HANDLE_CURRENCY: str

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")
