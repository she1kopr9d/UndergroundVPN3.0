import pydantic


class StartDataANSW(pydantic.BaseModel):
    user_id: int
    status: str
