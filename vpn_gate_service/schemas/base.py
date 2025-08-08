import pydantic


class PagginatorData(pydantic.BaseModel):
    pass


class DefaultTelegramData(pydantic.BaseModel):
    user_id: int
    message_id: int
