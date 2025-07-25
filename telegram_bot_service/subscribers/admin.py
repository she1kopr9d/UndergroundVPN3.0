import rabbit
import deps
import schemas.admin


@rabbit.broker.subscriber("notification_auth_server")
async def handle_auth_server(
    data: schemas.admin.AuthServer,
):
    bot = await deps.get_bot()
    msg = (
        f"Сервер {data.server_name} ({data.server_ip}:"
        f"{data.server_port})"
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
