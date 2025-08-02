import content.config
import content.user
import deps
import keyboards
import rabbit
import schemas.config
import schemas.user


@rabbit.broker.subscriber("start_command_answer")
async def handle_start(
    data: schemas.user.StartDataANSW,
):
    bot = await deps.get_bot()
    msg = ""
    if (data.status == "registered") or (data.status == "user already exists"):
        msg = content.user.START_COMMAND(
            bot_username=((await bot.get_me()).username),
            ref_code=data.user_id,
        )
    else:
        msg = "Произошла непредвиденная ошибка"
    if data.is_referral:
        msg += content.user.REFERRAL_TEXT(
            data.referrer_username,
        )
    await bot.send_message(
        chat_id=data.user_id, text=msg, parse_mode="Markdown"
    )


@rabbit.broker.subscriber("create_config_answer")
async def handle_create_config(
    data: schemas.user.ConfigDataANSW,
):
    bot = await deps.get_bot()
    await bot.send_message(
        chat_id=data.user_id,
        text=content.user.VIEW_CONFIG(data.config_url),
        parse_mode="Markdown",
    )


@rabbit.broker.subscriber("new_referral")
async def handle_new_referral(
    data: schemas.user.NewReferralData,
):
    bot = await deps.get_bot()
    await bot.send_message(
        chat_id=data.referrer_user_id,
        text=content.user.NEW_REFERRAL(data.referral_username),
        parse_mode="Markdown",
    )


@rabbit.broker.subscriber("profile_command_answer")
async def profile_command_handler(
    data: schemas.user.ProfileData,
):
    bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text=content.user.PROFILE_COMMAND(
            data,
            bot_username=((await bot.get_me()).username),
        ),
        parse_mode="Markdown",
    )


@rabbit.broker.subscriber("ref_command_answer")
async def ref_command_handler(
    data: schemas.user.ReferralCommandData,
):
    bot = await deps.get_bot()
    kwargs = dict()
    if data.referrals:
        kwargs.update(
            {
                "reply_markup": keyboards.build_referrals_keyboard(data),
            }
        )

    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text=content.user.REF_COMMAND(
            referral_percentage=data.referral_percentage,
            referrer_username=data.referrer_username,
        ),
        parse_mode="Markdown",
        **kwargs,
    )


@rabbit.broker.subscriber("conf_command_answer")
async def conf_command_handler(
    data: schemas.config.ConfigPageANSW,
):
    bot = await deps.get_bot()
    kwargs = dict()
    if data.configs:
        kwargs.update(
            {
                "reply_markup": keyboards.build_configs_keyboard(data),
            }
        )

    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text="*Ваши конфиги*",
        parse_mode="Markdown",
        **kwargs,
    )


@rabbit.broker.subscriber("conf_info_command_answer")
async def conf_info_command_handler(
    data: schemas.config.ConfigInfoANSW,
):
    bot = await deps.get_bot()

    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text=content.config.CONFIG_INFO(data),
        reply_markup=keyboards.build_config_info_keyboard(data),
        parse_mode="Markdown",
    )
