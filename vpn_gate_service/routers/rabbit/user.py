import faststream.rabbit.fastapi

import schemas.telegram
import database.io.telegram_user
import config


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("start_command")
async def handle_start(data: schemas.telegram.StartData):
    print("Start command")
    status = ""
    referrer: None | schemas.telegram.UserAllData = None
    if await database.io.telegram_user.telegram_user_exist(data):
        status = "user already exists"
    else:
        if data.referrer_user_id is not None:
            referrer = await database.io.telegram_user.get_telegram_user_data(
                data.referrer_user_id,
            )
            await database.io.telegram_user.create_telegram_user(
                data,
                referrer.id,
            )
            await router.broker.publish(
                {
                    "referrer_user_id": referrer.user_id,
                    "referral_username": data.username,
                },
                queue="new_referral",
            )
        else:
            await database.io.telegram_user.create_telegram_user(data)
        status = "registered"

    await router.broker.publish(
        {
            "user_id": data.user_id,
            "status": status,
            "is_referral": referrer is not None,
            "referrer_username": (referrer.username if referrer else None),
        },
        queue="start_command_answer",
    )
