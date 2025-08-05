import schemas.moderator


def MODERATION_PAYMENT(
    data: schemas.moderator.PaymentModerCellData,
) -> str:
    return f"""
Проверьте верность платежа

Платеж {data.payment.payment_id}
Метод: {data.payment.payment_method}
Сумма: {data.payment.amount}

Пользователь @{data.user.username}
"""
