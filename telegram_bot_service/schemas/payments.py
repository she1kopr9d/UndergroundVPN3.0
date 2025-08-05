import typing
import pydantic

import schemas.base


class PaymentInfo(pydantic.BaseModel):
    payment_id: int
    payment_method: str


class PaymentPageANSW(
    schemas.base.BasePage,
    schemas.base.DefaultTelegramANSW,
):
    payments: typing.List[PaymentInfo] | None


class PaymentIdANSW(
    schemas.base.DefaultTelegramANSW
):
    payment_id: int


# class ConfigInfoANSW(pydantic.BaseModel):
#     user_id: int
#     message_id: int
#     config_id: int
#     config_name: str
#     config_url: str
#     server_id: int
#     server_name: str
#     now_page: int
