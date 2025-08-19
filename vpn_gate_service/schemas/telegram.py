import typing

import pydantic


class StartData(pydantic.BaseModel):
    user_id: int
    username: str
    referrer_user_id: int | None


class ProfileData(pydantic.BaseModel):
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


class PagginationPage(pydantic.BaseModel):
    user_id: int
    page: int
    pagination: int
    message_id: int


class RefPage(PagginationPage):
    pass


class ConfPage(PagginationPage):
    pass


class PayPage(PagginationPage):
    pass


class MarketPage(PagginationPage):
    pass


class Referral(pydantic.BaseModel):
    user_id: int
    username: str


class ReferralCommandData(pydantic.BaseModel):
    user_id: int
    referrals: typing.List[Referral]
    referral_percentage: int
    referrer_username: str | None
    max_page: int
    now_page: int


class PaymentMinInfo(pydantic.BaseModel):
    payment_id: int
    payment_method: str


class MessageData(pydantic.BaseModel):
    text: str | None
    photo: str | None
