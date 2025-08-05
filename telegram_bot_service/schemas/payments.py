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


class PaymentIdANSW(schemas.base.DefaultTelegramANSW):
    payment_id: int


class ReceiptData(pydantic.BaseModel):
    filename: str
    filebytes: str


class PaymentData(PaymentInfo):
    amount: float
    receipt: ReceiptData | None
