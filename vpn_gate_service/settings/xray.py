import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    DOMAIN: str
    VPN_PORT: int
    HOST: str
    FINGERPRINT: str
    ENCRYPTION: str
    SECURITY: str
    NET_TYPE: str
    SHORTID: str
    PUBLICKEY: str

    XRAY_CONTEINER: str

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")
