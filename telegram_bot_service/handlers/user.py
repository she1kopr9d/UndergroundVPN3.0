import aiogram
import aiogram.filters

import broker


router = aiogram.Router()


@router.message(aiogram.filters.CommandStart)
async def handle_start_command(message: aiogram.types.Message):
    await broker.broker_obj.publish(
        {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
        },
        queue="start_command",
    )
    await message.answer("Вы были зарегистрированы.")
