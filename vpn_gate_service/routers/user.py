import faststream.rabbit.fastapi

import config
import schemas.telegram
import database.io.telegram_user


router = faststream.rabbit.fastapi.RabbitRouter(
    url=config.rabbitmq.rabbitmq_url,
)


@router.post("/user/is_admin")
async def user_is_admin(data: schemas.telegram.UserData):
    is_admin = await database.io.telegram_user.user_is_admin(data)
    return {
        "status": "ok",
        "data": {
            "user": data,
            "is_admin": is_admin,
        },
    }


@router.post("/user/is_handle")
async def user_is_handle(data: schemas.telegram.UserData):
    is_handle = await database.io.telegram_user.user_is_handle(data)
    return {
        "status": "ok",
        "data": {
            "user": data,
            "is_handle": is_handle,
        },
    }
