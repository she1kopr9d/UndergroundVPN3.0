import aiogram
import aiogram.filters

import rabbit


router = aiogram.Router()


@router.message(aiogram.filters.CommandStart())
async def handle_start_command(message: aiogram.types.Message):
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
        },
        queue="start_command",
    )


@router.message(aiogram.filters.Command("test"))
async def handle_test_command(message: aiogram.types.Message):
    await message.answer("test command")
