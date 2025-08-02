import pydantic


class CreateConfig(pydantic.BaseModel):
    user_id: int
    server_name: str
    config_name: str


class ConfigInfo(pydantic.BaseModel):
    config_id: int
    config_name: str


class ConfigGetInfo(pydantic.BaseModel):
    user_id: int
    message_id: int
    config_id: int
    now_page: int
