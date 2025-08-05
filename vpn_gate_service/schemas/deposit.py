import pydantic


class DepositeCreate(pydantic.BaseModel):
    user_id: int
    message_id: int
    amount: int
    method: str


class DepositeMoveData(pydantic.BaseModel):
    user_id: int
    message_id: int
    payment_id: int
