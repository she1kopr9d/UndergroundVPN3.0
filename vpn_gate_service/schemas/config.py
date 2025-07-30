import pydantic


class CreateConfig(pydantic.BaseModel):
    user_id: int
    server_name: str
