import aiogram
import aiogram.filters

import rabbit
import content.user
import callback


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
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
        },
        queue="profile_command",
    )


@router.message(aiogram.filters.Command("ref"))
async def ref_command_handler(message: aiogram.types.Message):
    sent_message = await message.answer("Загружаю...")
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "page": 0,
            "pagination": 3,
            "message_id": sent_message.message_id,
        },
        queue="ref_command",
    )


@router.callback_query(callback.ReferralPageCallback.filter())
async def ref_page_query(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.ReferralPageCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "page": callback_data.page,
            "pagination": 3,
            "message_id": callback_data.message_id,
        },
        queue="ref_command",
    )
