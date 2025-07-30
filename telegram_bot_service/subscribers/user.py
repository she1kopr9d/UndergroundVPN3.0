import rabbit
import deps
import schemas.user

import content.user


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
