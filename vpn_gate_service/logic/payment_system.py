import database.models

import config


def get_amount(
    amount: int,
    method: database.models.PaymentMethod,
) -> float:
    if method == database.models.PaymentMethod.telegram_star.value:
        amount *= 2.5
    elif method == database.models.PaymentMethod.crypto.value:
        amount /= 78
    return float(amount)


def get_requisite(
    method: database.models.PaymentMethod,
):
    match method:
        case database.models.PaymentMethod.crypto.value:
            return (
                (
                    f"<code>{config.payment.CRYPTO_ADDRESS}</code>"
                    " cистема - "
                    f"{config.payment.CRYPTO_WEB}"
                ),
                "USDT",
            )
        case database.models.PaymentMethod.telegram_star.value:
            return (None, "STAR")
        case database.models.PaymentMethod.handle.value:
            return (
                config.payment.HANDLE_ADDRESS,
                config.payment.HANDLE_CURRENCY,
            )
        case database.models.PaymentMethod.system.value:
            return ("Тестовые реквизиты для тестов", "BTC")
