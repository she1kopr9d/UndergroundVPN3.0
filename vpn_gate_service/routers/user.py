import config
import database.io.moderator
import database.io.telegram_user
import faststream.rabbit.fastapi
import schemas.telegram

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


@router.post("/user/is_moderator")
async def user_is_moderator(data: schemas.telegram.UserData):
    user_obj = await database.io.telegram_user.get_telegram_user_data(
        data.user_id,
    )
    is_moderator = await database.io.moderator.is_moderator(user_obj.id)
    return {
        "status": "ok",
        "data": {
            "user": data,
            "is_moderator": is_moderator,
        },
    }
