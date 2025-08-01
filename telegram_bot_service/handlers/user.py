import aiogram
import aiogram.filters

import rabbit
import content.user


router = aiogram.Router()


@router.message(aiogram.filters.CommandStart(deep_link=True))
async def handle_start_command_deep_link(
    message: aiogram.types.Message,
    command: aiogram.filters.CommandStart,
):
    if not message.from_user.username:
        await message.answer(
            "К сожалению я не могу работать с пользователями без username"
        )
        return
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "referrer_user_id": int(command.args),
        },
        queue="start_command",
    )


@router.message(aiogram.filters.CommandStart(deep_link=False))
async def handle_start_command(
    message: aiogram.types.Message,
):
    if not message.from_user.username:
        await message.answer(
            "К сожалению я не могу работать с пользователями без username"
        )
        return
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "referrer_user_id": None,
        },
        queue="start_command",
    )


@router.message(aiogram.filters.Command("help"))
async def handle_help_command(message: aiogram.types.Message):
    await message.answer(
        text=content.user.HELP_COMMAND(),
        parse_mode="HTML",
    )


@router.message(aiogram.filters.Command("profile"))
async def handle_profile_command(message: aiogram.types.Message):
    await message.answer("Здесь будет реализона команда /profile")
