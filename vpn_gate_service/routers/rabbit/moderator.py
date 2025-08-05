import faststream.rabbit.fastapi

import config
import schemas.telegram
import database.io.payments
import database.io.moderator


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("pay_list_command")
async def pay_list_handler(
    data: schemas.telegram.PayPage,
):
    payments, max_page = (
        await database.io.payments.get_moderation_payments_with_pagination(
            data,
        )
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
            "max_page": max_page,
            "now_page": data.page,
            "payments": payments,
        },
        queue="pay_list_command_answer",
    )


@router.subscriber("new_moderation_payment")
async def new_moderation_payment_alert():
    moderators_ids = (
        await database.io.moderator.get_moderator_telegram_id_list()
    )
    for moderator_id in moderators_ids:
        await router.broker.publish(
            {
                "user_id": moderator_id,
            },
            queue="new_moderation_payment_alert"
        )
