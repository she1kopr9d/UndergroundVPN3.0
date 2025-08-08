import aiogram
import content.user
import keyboards
import logic.payments
import rabbit
import schemas.config
import schemas.user


async def main_menu(
    bot: aiogram.Bot,
    chat_id: int,
    message_id: int = None,
) -> int:
    if message_id is None:
        send_message = await bot.send_message(
            chat_id=chat_id,
            text="Загружаю...",
        )
        message_id = send_message.message_id
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Главное меню",
        reply_markup=keyboards.build_main_menu_keyboard(
            user_id=chat_id,
            message_id=message_id,
        ),
    )
    return message_id


async def profile_menu(
    bot: aiogram.Bot,
    data: schemas.user.ProfileData,
    message_id: int,
):
    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=message_id,
        text=content.user.PROFILE_COMMAND(
            data,
            bot_username=((await bot.get_me()).username),
        ),
        reply_markup=keyboards.build_back_to_main_menu_keyboard(
            user_id=data.user_id,
            message_id=message_id,
        ),
        parse_mode="HTML",
    )


async def referral_menu(
    bot: aiogram.Bot,
    data: schemas.user.ReferralCommandData,
):
    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text=content.user.REF_COMMAND(
            referral_percentage=data.referral_percentage,
            referrer_username=data.referrer_username,
        ),
        parse_mode="HTML",
        reply_markup=keyboards.build_referrals_keyboard(data),
    )


async def config_menu(
    bot: aiogram.Bot,
    data: schemas.config.ConfigPageANSW,
) -> None:
    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text="*Ваши конфиги*",
        parse_mode="Markdown",
        reply_markup=keyboards.build_configs_keyboard(data),
    )


async def deposit_menu(
    user_id: int,
    message_id: int,
    bot: aiogram.Bot,
):
    deposit_data = await logic.payments.get_payment_methods(
        user_id,
    )
    await bot.edit_message_text(
        text="Выберите метод оплаты",
        chat_id=user_id,
        message_id=message_id,
        reply_markup=keyboards.build_deposit_keyboard(
            user_id=user_id,
            message_id=message_id,
            payment_methods=deposit_data["payment_methods"],
        ),
    )


async def market_menu(
    user_id: int,
    message_id: int,
    bot: aiogram.Bot,
):
    await bot.edit_message_text(
        text="Маркет",
        chat_id=user_id,
        message_id=message_id,
        reply_markup=keyboards.build_market_list_keyboard(
            user_id,
            message_id,
        ),
    )


async def profile_menu_request(
    user_id: int,
) -> None:
    await rabbit.broker.publish(
        {
            "user_id": user_id,
        },
        queue="profile_command",
    )
