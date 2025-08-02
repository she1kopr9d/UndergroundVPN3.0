import aiogram
import aiogram.types
import aiogram.filters

import config
import rabbit


router: aiogram.Router = aiogram.Router()


@router.message(aiogram.filters.Command("handle"))
async def handle_command(message: aiogram.types.Message):
    if len(message.text.split()) < 2:
        return
    if message.text.split()[1] != config.settings.HANDLE_CODE:
        return
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
        },
        queue="handle_add",
    )


@router.message(aiogram.filters.Command("deposit"))
async def deposit_command(message: aiogram.types.Message):
    pass
