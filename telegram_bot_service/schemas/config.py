import typing

import pydantic
import schemas.base


class ConfigInfo(pydantic.BaseModel):
    config_id: int
    config_name: str


class ConfigPageANSW(schemas.base.BasePage):
    user_id: int
    message_id: int
    configs: typing.List[ConfigInfo] | None


class ConfigInfoANSW(pydantic.BaseModel):
    user_id: int
    message_id: int
    config_id: int
    config_name: str
    config_url: str
    server_id: int
    server_name: str
    now_page: int
