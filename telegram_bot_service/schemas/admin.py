import pydantic


class AuthServer(pydantic.BaseModel):
    user_id: int
    server_name: str
    server_ip: str
    server_port: int
    status: str
