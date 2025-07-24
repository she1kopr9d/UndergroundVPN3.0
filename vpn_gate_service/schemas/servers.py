import pydantic


class ServerAuth(pydantic.BaseModel):
    name: str = pydantic.Field(..., description="Имя сервера")
    ip: str = pydantic.Field(..., description="IP сервера")
    port: int = pydantic.Field(..., ge=1, le=65535, description="Порт сервера")
    api_version: str = pydantic.Field(..., description="Версия API на сервере")
    secret_key: str = pydantic.Field(
        ..., description="Секретный ключ для авторизации"
    )


class ServerPublicInfo(pydantic.BaseModel):
    name: str = pydantic.Field(..., description="Имя сервера")
    ip: str = pydantic.Field(..., description="IP сервера")
    port: int = pydantic.Field(..., ge=1, le=65535, description="Порт сервера")
    api_version: str
