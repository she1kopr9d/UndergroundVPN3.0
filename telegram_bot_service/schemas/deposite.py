import pydantic


class DepositeCreateANSW(pydantic.BaseModel):
    user_id: int
    message_id: int
    payment_id: int
    requisite: str | None
    currency: str | None
    amount: float
    method: str


class WithdrawalInfo(pydantic.BaseModel):
    user_id: int
    amount: float
    now_balance: float
    status: str
