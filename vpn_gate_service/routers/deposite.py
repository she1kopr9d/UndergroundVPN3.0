import config
import database.io.base
import database.io.telegram_user
import database.models
import faststream.rabbit.fastapi
import schemas.deposit
import schemas.telegram

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


@router.post("/payment/method")
async def payment_method(
    data: schemas.deposit.DepositeId,
):
    payment_obj: database.models.Payment = (
        await database.io.base.get_object_by_id(
            id=data.payment_id,
            object_class=database.models.Payment,
        )
    )
    if payment_obj is None:
        return {"status": "object is none"}
    return {
        "status": "ok",
        "method": payment_obj.payment_method.value,
    }
