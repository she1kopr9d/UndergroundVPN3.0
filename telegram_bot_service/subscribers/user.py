import io

import aiogram.fsm.context
import content.config
import content.deposite
import content.product
import content.user
import deps
import keyboards
import logic.list_menu
import logic.menu
import rabbit
import schemas.base
import schemas.config
import schemas.deposite
import schemas.payments
import schemas.product
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
    await logic.menu.main_menu(bot, data.user_id)


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
    state: aiogram.fsm.context.FSMContext = await deps.get_state(data.user_id)
    state_data = await state.get_data()
    message_id = None
    try:
        message_id = state_data["message_id"]
    except Exception:
        send_message = await bot.send_message(
            chat_id=data.user_id, text="Загружаю..."
        )
        message_id = send_message.message_id
    finally:
        await state.clear()
    await logic.menu.profile_menu(
        bot,
        data,
        message_id,
    )


@rabbit.broker.subscriber("ref_command_answer")
async def ref_command_handler(
    data: schemas.user.ReferralCommandData,
):
    bot = await deps.get_bot()
    await logic.menu.referral_menu(bot, data)


@rabbit.broker.subscriber("conf_command_answer")
async def conf_command_handler(
    data: schemas.config.ConfigPageANSW,
):
    bot = await deps.get_bot()
    await logic.menu.config_menu(bot, data)


@rabbit.broker.subscriber("market_command_answer")
async def market_command_handler(
    data: schemas.product.ProductListData,
):
    bot = await deps.get_bot()
    await logic.menu.market_menu(bot, data)


@rabbit.broker.subscriber("conf_info_command_answer")
async def conf_info_command_handler(
    data: schemas.config.ConfigInfoANSW,
):
    bot = await deps.get_bot()

    kb = None
    if data.end_date is None:
        kb = keyboards.build_config_info_keyboard
    elif data.status == "canceled":
        kb = keyboards.build_resub_config_info_keyboard
    else:
        kb = keyboards.build_sub_config_info_keyboard
    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text=content.config.CONFIG_INFO(data),
        reply_markup=kb(data),
        parse_mode="HTML",
    )


@rabbit.broker.subscriber("delete_config_command_answer")
async def delete_config_command_handler(
    data: schemas.base.DefaultTelegramANSW,
):
    await logic.list_menu.publish_list_menu(
        "conf_command",
        data.user_id,
        data.message_id,
    )


@rabbit.broker.subscriber("handle_add_answer")
async def handle_add_handler(
    data: schemas.user.UserIdANSW,
):
    bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text=(
            "Поздравляю, теперь я уверен, что вам можно"
            " доверять, теперь у вас доступен способ "
            "пополнения напрямую мне на карточку. Приятного пользования"
        ),
    )


@rabbit.broker.subscriber("create_payment_answer")
async def create_payment_handler(
    data: schemas.deposite.DepositeCreateANSW,
):
    bot = await deps.get_bot()

    link = None
    if data.method == "telegram_star":
        prices = [aiogram.types.LabeledPrice(label="XTR", amount=data.amount)]
        link = await bot.create_invoice_link(
            title="Пополнение баланса в боте",
            description=f"Пополнить баланс на {data.amount/2.5} рублей",
            prices=prices,
            provider_token="",
            payload="channel_support",
            currency="XTR",
        )

    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text=content.deposite.DEPOSITE_INFO(data),
        reply_markup=keyboards.build_payment_accept_keyboard(
            data=data,
            link=link,
        ),
        parse_mode="HTML",
    )


@rabbit.broker.subscriber("accept_deposit_answer")
async def accept_deposit_handler(
    data: schemas.payments.PaymentIdANSW,
):
    bot = await deps.get_bot()
    try:
        await bot.edit_message_reply_markup(
            chat_id=data.user_id,
            message_id=data.message_id,
            reply_markup=None,
        )
    except Exception as error:
        print(f"{error}")
    await bot.send_message(
        chat_id=data.user_id,
        text=(
            "Ваш платеж в обработке, модерация проверит "
            "его, после мы вам пополним баланс \n\n"
            "Обычно это занимает не более 15 минут"
        ),
    )


async def deposit_moder_to_client(
    data: schemas.user.UserIdANSW,
    text: str,
):
    bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text=text,
    )


@rabbit.broker.subscriber("cancel_deposit_moder_to_client")
async def cancel_deposit_moder_to_client_handler(
    data: schemas.user.UserIdANSW,
):
    await deposit_moder_to_client(
        data=data,
        text="Модерация не нашла платеж в системе",
    )


@rabbit.broker.subscriber("accept_deposit_moder_to_client")
async def accept_deposit_moder_to_client_handler(
    data: schemas.base.DefaultTelegramANSW,
):
    bot = await deps.get_bot()
    try:
        await bot.edit_message_reply_markup(
            chat_id=data.user_id,
            message_id=data.message_id,
        )
    except Exception:
        pass
    await deposit_moder_to_client(
        data=data,
        text="Модерация одобрила ваш платеж, в /profile пополнился баланс",
    )


@rabbit.broker.subscriber("now_referral_deposit")
async def now_referral_deposit_handler(
    data: schemas.user.ReferralDepositInfo,
):
    bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text=content.user.REFERRAL_DEPOSIT(data),
    )


@rabbit.broker.subscriber("crypto_payment_not_paid")
async def crypto_payment_not_paid_handler(
    data: schemas.base.DefaultTelegramANSW,
):
    bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text="Платеж не найден, либо он в обработке.",
    )


@rabbit.broker.subscriber("product_info_answer")
async def product_info_handler(
    data: schemas.product.ProductView,
):
    bot = await deps.get_bot()

    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text=content.product.PRODUCT_INFO(data),
        reply_markup=keyboards.build_product_info_keyboard(data),
        parse_mode="HTML",
    )


@rabbit.broker.subscriber("execute_withdrawal_payment")
async def execute_withdrawal_payment_handler(
    data: schemas.deposite.WithdrawalInfo,
):
    bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text=content.deposite.WITHDRAWAL_INFO(data),
        parse_mode="HTML",
    )


@rabbit.broker.subscriber("error_withdrawal_payment")
async def error_withdrawal_payment_handler(
    data: schemas.deposite.WithdrawalInfo,
):
    bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text=content.deposite.ERROR_WITHDRAWAL_INFO(data),
        parse_mode="HTML",
    )


@rabbit.broker.subscriber("send_telegram_message")
async def send_telegram_message_handler(
    data: schemas.user.MessageData,
):
    bot = await deps.get_bot()

    user_id = data.user_id
    text = data.text
    photo = data.photo
    try:
        if photo:
            file_bytes = data.photo.encode("latin1")
            file_name_plug = "news.jpg"
            file_like = io.BytesIO(file_bytes)
            file_like.name = file_name_plug
            photo = aiogram.types.BufferedInputFile(
                file=file_like.getvalue(),
                filename=file_name_plug,
            )
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=text or "",
            )
        elif text:
            await bot.send_message(chat_id=user_id, text=text)
        else:
            await bot.send_message(chat_id=user_id, text="(пустая новость)")
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
