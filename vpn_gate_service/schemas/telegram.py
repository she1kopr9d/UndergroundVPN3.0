import pydantic


class StartData(pydantic.BaseModel):
    user_id: int
    username: str
