import io

import aiogram
import content.moderation
import deps
import keyboards
import logic.list_menu
import rabbit
import schemas.base
import schemas.moderator
import schemas.payments
import schemas.user


@rabbit.broker.subscriber("pay_list_command_answer")
async def pay_list_handler(
    data: schemas.payments.PaymentPageANSW,
):
    bot: aiogram.Bot = await deps.get_bot()

    await bot.edit_message_text(
        chat_id=data.user_id,
        message_id=data.message_id,
        text="Панель модерации платежей",
        reply_markup=keyboards.build_payments_keyboard(
            data,
        ),
    )


@rabbit.broker.subscriber("new_moderation_payment_alert")
async def new_moderation_payment_alert_handler(
    data: schemas.user.UserIdANSW,
):
    bot: aiogram.Bot = await deps.get_bot()

    await bot.send_message(
        chat_id=data.user_id,
        text="Новый запрос на модерации, чтобы увидеть, нажмите /pay_list",
    )


@rabbit.broker.subscriber("pay_cell_moder_data_answer")
async def pay_cell_moder_data_handler(
    data: schemas.moderator.PaymentModerCellData,
):
    bot: aiogram.Bot = await deps.get_bot()

    if data.payment.receipt:
        await bot.delete_message(
            chat_id=data.user_id,
            message_id=data.message_id,
        )
        file_bytes = data.payment.receipt.filebytes.encode("latin1")

        file_like = io.BytesIO(file_bytes)
        file_like.name = data.payment.receipt.filename
        photo = aiogram.types.BufferedInputFile(
            file=file_like.getvalue(),
            filename=data.payment.receipt.filename,
        )
        send_message = await bot.send_photo(
            chat_id=data.user_id,
            photo=photo,
            caption=content.moderation.MODERATION_PAYMENT(data),
            reply_markup=None,
        )
        await bot.edit_message_reply_markup(
            chat_id=data.user_id,
            message_id=send_message.message_id,
            reply_markup=keyboards.build_moderator_accept_keyboard(
                data,
                send_message.message_id,
            ),
        )
    else:
        await bot.edit_message_text(
            chat_id=data.user_id,
            message_id=data.message_id,
            text=content.moderation.MODERATION_PAYMENT(data),
            reply_markup=keyboards.build_moderator_accept_keyboard(
                data,
                data.message_id,
            ),
        )


async def deposit_moder_answer_handler(
    data: schemas.base.DefaultTelegramANSW,
    caption: str,
):
    bot: aiogram.Bot = await deps.get_bot()

    try:
        await bot.edit_message_caption(
            chat_id=data.user_id,
            message_id=data.message_id,
            caption=caption,
            reply_markup=None,
        )
    except Exception:
        await bot.edit_message_text(
            chat_id=data.user_id,
            message_id=data.message_id,
            text=caption,
            reply_markup=None,
        )
    await logic.list_menu.load_page_handler_bot(
        bot=bot,
        user_id=data.user_id,
        queue="pay_list_command",
    )


@rabbit.broker.subscriber("cancel_deposit_moder_answer")
async def cancel_deposit_moder_answer_handler(
    data: schemas.base.DefaultTelegramANSW,
):
    await deposit_moder_answer_handler(data, "Отказ")


@rabbit.broker.subscriber("accept_deposit_moder_answer")
async def accept_deposit_moder_answer_handler(
    data: schemas.base.DefaultTelegramANSW,
):
    await deposit_moder_answer_handler(data, "Подтвержденно")
