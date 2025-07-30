import faststream.rabbit.fastapi

import schemas.telegram
import database.io.telegram_user
import config


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("start_command")
async def handle_start(data: schemas.telegram.StartData):
    status = ""
    if await database.io.telegram_user.telegram_user_exist(data):
        status = "user already exists"
    else:
        await database.io.telegram_user.create_telegram_user(data)
        status = "registered"
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "status": status,
        },
        queue="start_command_answer",
    )
