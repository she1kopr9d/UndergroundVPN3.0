import rabbit
import deps
import schemas.admin
import schemas.user


@rabbit.broker.subscriber("notification_auth_server")
async def handle_auth_server(
    data: schemas.admin.AuthServer,
):
    bot = await deps.get_bot()
    msg = (
        f"Сервер {data.server_name} ({data.server_ip}:" f"{data.server_port})"
    )
    if data.status == "start":
        msg += " запущен"
    elif data.status == "stop":
        msg += " выключен"
    else:
        msg += f" нестандартный статус {data.status}"
    await bot.send_message(
        chat_id=data.user_id,
        text=msg,
    )


@rabbit.broker.subscriber("create_server_answer")
async def handle_create_server(
    data: schemas.user.StatusDataANSW,
):
    bot = await deps.get_bot()
    if data.status != "ok":
        await bot.send_message(
            chat_id=data.user_id,
            text="Произошла непредвиденная ошибка при создании сервера",
        )
        return
    await bot.send_message(
        chat_id=data.user_id,
        text="Сервер успешно создан",
    )
