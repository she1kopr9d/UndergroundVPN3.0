import faststream.rabbit.fastapi

import config
import schemas.telegram
import database.models
import database.io.telegram_user


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.post("/deposit/list")
async def deposite_list_router(
    data: schemas.telegram.UserData,
):
    is_handle = await database.io.telegram_user.user_is_handle(
        data,
    )
    is_admin = await database.io.telegram_user.user_is_handle(
        data,
    )
    dep_method = [
        {
            "title": "Звездами телеграм",
            "method": database.models.PaymentMethod.telegram_star,
        },
        {
            "title": "Криптовалютой",
            "method": database.models.PaymentMethod.crypto,
        },
    ]
    if is_handle:
        dep_method.append(
            {
                "title": "В ручную (СБП)",
                "method": database.models.PaymentMethod.handle,
            },
        )
    if is_admin:
        dep_method.append(
            {
                "title": "Системная",
                "method": database.models.PaymentMethod.system,
            },
        )
    return {
        "status": "ok",
        "payment_methods": dep_method,
    }
