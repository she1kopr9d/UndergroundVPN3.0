import typing

import pydantic


class UserIdANSW(pydantic.BaseModel):
    user_id: int


class UserViewData(UserIdANSW):
    username: str


class StartDataANSW(UserIdANSW):
    status: str
    is_referral: bool
    referrer_username: str | None


class ConfigDataANSW(UserIdANSW):
    config_url: str


class StatusDataANSW(UserIdANSW):
    status: str


class NewReferralData(pydantic.BaseModel):
    referrer_user_id: int
    referral_username: str | None


class ProfileData(UserViewData):
    referral_percentege: int
    balance: float


class Referral(UserViewData):
    pass


class ReferralCommandData(UserIdANSW):
    referrals: typing.List[Referral] | None
    referral_percentage: int
    referrer_username: str | None
    message_id: int
