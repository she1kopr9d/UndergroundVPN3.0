import pydantic


class StartDataANSW(pydantic.BaseModel):
    user_id: int
    status: str


class ConfigDataANSW(pydantic.BaseModel):
    user_id: int
    config_url: str


class StatusDataANSW(pydantic.BaseModel):
    user_id: int
    status: str
