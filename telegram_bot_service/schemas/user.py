import typing

import pydantic
import schemas.base


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


class ReferralData(pydantic.BaseModel):
    referrer_user_id: int
    referral_username: str | None


class ReferralInfoData(pydantic.BaseModel):
    referral_user_id: int
    referral_username: str | None


class NewReferralData(ReferralData):
    pass


class ProfileData(UserViewData):
    referral_percentege: int
    balance: float


class Referral(UserViewData):
    pass


class ReferralCommandData(
    schemas.base.DefaultTelegramANSW,
    schemas.base.BasePage,
):
    referrals: typing.List[Referral] | None
    referral_percentage: int
    referrer_username: str | None


class ReferralDepositInfo(
    ReferralInfoData,
    UserIdANSW,
):
    amount: float


class MessageData(
    pydantic.BaseModel,
):
    user_id: int
    text: str | None
    photo: str | None
