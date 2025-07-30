import pydantic


class AddAdmin(pydantic.BaseModel):
    user_id: int
    secret_key: str
