import pydantic
import typing


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


class ProfileData(pydantic.BaseModel):
    user_id: int
    username: str
    referral_percentege: int
    balance: float


class Referral(pydantic.BaseModel):
    user_id: int
    username: str


class ReferralCommandData(pydantic.BaseModel):
    user_id: int
    referrals: typing.List[Referral] | None
    referral_percentage: int
    referrer_username: str | None
    max_page: int
    now_page: int
    message_id: int
