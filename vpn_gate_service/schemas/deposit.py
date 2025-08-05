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


class DepositeId(pydantic.BaseModel):
    payment_id: int


class DepositReceiptUploadData(DepositeMoveData):
    filename: str
    filebytes: str


class DepositCellData(DepositeMoveData):
    now_page: int
