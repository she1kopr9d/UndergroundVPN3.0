import aiogram
import aiogram.types
import aiogram.filters
import aiogram.fsm.context

import config
import rabbit
import keyboards
import logic.payments
import callback
import states


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
    deposit_data = await logic.payments.get_payment_methods(
        message.from_user.id,
    )
    await message.answer(
        text="Выберите метод оплаты",
        reply_markup=keyboards.build_deposit_keyboard(
            user_id=message.from_user.id,
            payment_methods=deposit_data["payment_methods"],
        ),
    )


@router.callback_query(callback.DepositCallback.filter())
async def deposit_amount_query(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositCallback,
    state: aiogram.fsm.context.FSMContext,
):
    send_message = await query.message.edit_text(
        text="Введите число пополнения в РУБЛЯХ!",
        reply_markup=None,
    )
    await state.set_state(states.DepositForm.amount)
    await state.update_data(
        user_id=callback_data.user_id,
        method=callback_data.deposit_method,
        message_id=send_message.message_id,
    )


@router.message(states.DepositForm.amount)
async def check_valid_amount_handler(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    data = await state.get_data()
    text = message.text
    await message.delete()
    if not text.isdigit():
        await message.bot.edit_message_text(
            chat_id=data["user_id"],
            message_id=data["message_id"],
            text=(
                "Вы ввели не число, проверте сообщение\n"
                "Введите число пополнения в РУБЛЯХ!"
            ),
        )
    else:
        await state.clear()
        await logic.payments.create_payment(
            user_id=data["user_id"],
            message_id=data["message_id"],
            amount=int(text),
            method=data["method"],
        )
        await message.bot.edit_message_text(
            chat_id=data["user_id"],
            message_id=data["message_id"],
            text=("Загрузка..."),
        )
