import faststream.rabbit.fastapi

import config
import schemas.telegram
import database.io.telegram_user


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("start_command")
async def start_command_handler(data: schemas.telegram.StartData):
    await database.io.telegram_user.create_telegram_user(data)
