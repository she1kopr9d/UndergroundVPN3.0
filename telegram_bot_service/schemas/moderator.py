import schemas.payments
import schemas.user


class PaymentModerCellData(schemas.user.UserIdANSW):
    user: schemas.user.UserViewData
    message_id: int
    now_page: int
    payment: schemas.payments.PaymentData
