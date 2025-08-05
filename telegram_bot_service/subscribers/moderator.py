import aiogram

import deps
import rabbit
import keyboards
import schemas.payments
import schemas.base
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
