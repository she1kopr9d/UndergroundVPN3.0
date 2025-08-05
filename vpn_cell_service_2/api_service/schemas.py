import config
import pydantic


class ConfigEditInfo(pydantic.BaseModel):
    email: str
    uuid: pydantic.UUID4
    secret_key: str

    @pydantic.field_validator("secret_key")
    def check_secret_key(cls, v):
        if v != config.settings.GATE_SECRET_KEY:
            raise ValueError("Secret key is wrong")
        return v

    @property
    def client_data(self) -> dict:
        return {
            "email": str(self.email),
            "id": str(self.uuid),
            "flow": "xtls-rprx-vision",
            "level": 0,
        }
