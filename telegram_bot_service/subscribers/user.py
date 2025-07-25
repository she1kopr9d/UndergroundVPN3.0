import rabbit
import deps
import schemas.user


@rabbit.broker.subscriber("start_command_answer")
async def handle_start(
    data: schemas.user.StartDataANSW,
):
    bot = await deps.get_bot()
    msg = ""
    if data.status == "registered":
        msg = "Добро пожаловать"
    elif data.status == "user already exists":
        msg = "Вы успешно зарегистрировались"
    else:
        msg = "Произошла непредвиденная ошибка"
    await bot.send_message(
        chat_id=data.user_id,
        text=msg,
    )
