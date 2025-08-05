import config
import database.io.telegram_user
import fastapi
import faststream.rabbit.fastapi
import schemas.dev

router = faststream.rabbit.fastapi.RabbitRouter(
    url=config.rabbitmq.rabbitmq_url,
)


@router.post("/dev/add_admin")
async def add_admin_router(data: schemas.dev.AddAdmin):
    if data.secret_key != "qwerty.1":
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid secret key"
        )
    await database.io.telegram_user.set_admin(data)
    return {
        "status": "ok",
    }
