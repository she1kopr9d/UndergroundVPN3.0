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


async def load_page_handler(
    message: aiogram.types.Message,
    queue: str,
):
    sent_message = await message.answer("Загружаю...")
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "page": 0,
            "pagination": 3,
            "message_id": sent_message.message_id,
        },
        queue=queue,
    )


@router.message(aiogram.filters.Command("ref"))
async def ref_command_handler(message: aiogram.types.Message):
    await load_page_handler(message, "ref_command")


@router.message(aiogram.filters.Command("conf"))
async def conf_command_handler(message: aiogram.types.Message):
    await load_page_handler(message, "conf_command")


@router.callback_query(
    callback.PageCallback.filter()
)
async def page_query(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.PageCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "page": callback_data.page,
            "pagination": 3,
            "message_id": callback_data.message_id,
        },
        queue=f"{callback_data.move}_command",
    )


@router.callback_query(callback.ReferralCallback.filter())
async def ref_user_query(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.ReferralCallback,
):
    await query.message.answer(
        (
            "Этот функционал пока в разработке, не переживайте,"
            " мы ведем подсчет о ваших рефералах"
        )
    )
    # await rabbit.broker.publish(
    #     {
    #         "user_id": callback_data.user_id,
    #         "page": callback_data.page,
    #         "pagination": 3,
    #         "message_id": callback_data.message_id,
    #     },
    #     queue="ref_command",
    # )


@router.callback_query(
    callback.ConfigCallback.filter(
        aiogram.F.action == "open"
    )
)
async def conf_user_query(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.ConfigCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "message_id": callback_data.message_id,
            "config_id": callback_data.config_id,
            "now_page": callback_data.page,
        },
        queue="conf_info_command",
    )


@router.callback_query(
    callback.ConfigCallback.filter(
        aiogram.F.action == "back"
    )
)
async def conf_user_back_query(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.ConfigCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "page": callback_data.page,
            "pagination": 3,
            "message_id": callback_data.message_id,
        },
        queue="conf_command",
    )
