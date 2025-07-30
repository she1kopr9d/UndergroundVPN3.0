import pydantic


class StartData(pydantic.BaseModel):
    user_id: int
    username: str


class UserData(pydantic.BaseModel):
    user_id: int


class UserAllData(pydantic.BaseModel):
    id: int
    user_id: int
    username: str
    is_admin: bool


class CreateServerData(pydantic.BaseModel):
    user_id: int
    name: str
    secret_key: str
