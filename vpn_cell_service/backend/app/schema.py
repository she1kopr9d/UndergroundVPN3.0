import pydantic


class UserInput(pydantic.BaseModel):
    email: pydantic.EmailStr
    uuid: pydantic.UUID4
