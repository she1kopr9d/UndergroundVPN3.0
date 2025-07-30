import pydantic


class StartDataANSW(pydantic.BaseModel):
    user_id: int
    status: str
    is_referral: bool
    referrer_username: str | None


class ConfigDataANSW(pydantic.BaseModel):
    user_id: int
    config_url: str


class StatusDataANSW(pydantic.BaseModel):
    user_id: int
    status: str


class NewReferralData(pydantic.BaseModel):
    referrer_user_id: int
    referral_username: str | None
