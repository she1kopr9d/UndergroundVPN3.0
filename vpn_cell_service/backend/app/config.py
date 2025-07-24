import pathlib
import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    config_path: pathlib.Path = pydantic.Field(default="/etc/xray/config.json")
    xray_binary: pathlib.Path = pydantic.Field(default="/usr/local/bin/xray")
    restart_command: list[str] = pydantic.Field(
        default_factory=lambda: ["systemctl", "restart", "xray"]
    )
    inbound_tag: str = pydantic.Field(default="reality-inbound")
    SERVER_NAME: str = pydantic.Field(default="")
    IP_ADDRESS: str = pydantic.Field(default="")
    PORT: str = pydantic.Field(default="")
    GATE_SECRET_KEY: str = pydantic.Field(default="")
    GATE_API_VERSION: str = pydantic.Field(default="")
    GATE_IP_ADDRESS: str = pydantic.Field(default="")

    class Config:
        env_file = ".env"


settings = Settings()
