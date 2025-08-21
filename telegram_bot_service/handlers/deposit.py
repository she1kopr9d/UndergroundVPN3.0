import uuid

import aiogram
import aiogram.filters
import aiogram.fsm.context
import aiogram.types
import callback
import config
import keyboards
import logic.menu
import logic.payments
import rabbit
import states
import utils.types

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
    send_message = await message.answer(
        text="Загружаю...",
    )
    await logic.menu.deposit_menu(
        user_id=message.from_user.id,
        message_id=send_message.message_id,
        bot=message.bot,
    )


@router.callback_query(callback.DepositCallback.filter())
async def deposit_amount_query(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositCallback,
    state: aiogram.fsm.context.FSMContext,
):
    send_message = await query.message.edit_text(
        text="Введите число пополнения в РУБЛЯХ!",
        reply_markup=keyboards.build_back_to_menu_keyboard(
            callback_data.user_id,
            query.message.message_id,
            "dep",
        ),
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
        if int(text) > 100000:
            await message.bot.edit_message_text(
                chat_id=data["user_id"],
                message_id=data["message_id"],
                text=(
                    "Вы ввели число больше 100000 рублей\n"
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


@router.callback_query(
    callback.DepositAcceptCallback.filter(
        aiogram.F.action == "accept",
    )
)
async def accept_deposit_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositAcceptCallback,
    state: aiogram.fsm.context.FSMContext,
):
    method = await logic.payments.get_payment_method(
        payment_id=callback_data.payment_id,
    )
    if method in ["handle", "system"]:
        await state.set_state(states.DepositeReceiptForm.file)
        await state.update_data(
            user_id=callback_data.user_id,
            message_id=callback_data.message_id,
            payment_id=callback_data.payment_id,
        )
        await query.message.bot.edit_message_reply_markup(
            chat_id=callback_data.user_id,
            message_id=callback_data.message_id,
            reply_markup=None,
        )
        await query.message.answer(
            text=(
                "Пожалуйста скиньте скрин платежа, "
                "так модератор сможет проверить\n\n"
                "Нужна именно фотография/скрин НЕ ФАЙЛ!!!"
            )
        )
    else:
        await logic.payments.accept_deposit(callback_data)


@router.message(states.DepositeReceiptForm.file, aiogram.F.photo)
async def handle_receipt_photo(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
    bot: aiogram.Bot,
):
    data = await state.get_data()
    photo: aiogram.types.PhotoSize = message.photo[-1]
    telegram_file = await bot.get_file(photo.file_id)
    file_stream = await bot.download_file(telegram_file.file_path)
    file_bytes = file_stream.read()
    filename = f"{uuid.uuid4()}.jpg"
    await rabbit.broker.publish(
        {
            "user_id": data["user_id"],
            "message_id": data["message_id"],
            "payment_id": data["payment_id"],
            "filename": filename,
            "filebytes": file_bytes.decode("latin1"),
        },
        queue="save_payment_receipt",
    )
    await message.answer("✅ Чек получен и передан на проверку.")
    await state.clear()
    await logic.payments.accept_deposit(utils.types.DotDict(**data))


@router.callback_query(
    callback.DepositAcceptCallback.filter(
        aiogram.F.action == "cancel",
    )
)
async def cancel_deposit_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositAcceptCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "message_id": callback_data.message_id,
            "payment_id": callback_data.payment_id,
        },
        queue="cancel_deposit",
    )
    await query.message.delete()


async def send_file_to_queue(
    user_id: int,
    message_id: int,
    payment_id: int,
    file_id: str,
    file_name: str,
    file_bytes: bytes,
):
    await rabbit.broker.publish(
        {
            "file_id": file_id,
            "file_name": file_name,
            "file_bytes": file_bytes.decode("latin1"),
        },
        queue="upload_test_file",
    )


@router.message(aiogram.filters.Command("test_file"))
async def handle_document(
    message: aiogram.types.Message,
    bot: aiogram.Bot,
):
    if not message.document:
        await message.reply("Пожалуйста, пришли файл.")
        return

    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path
    file_name = message.document.file_name

    file_bytes = await bot.download_file(file_path)
    content = await file_bytes.read()

    await send_file_to_queue(
        file_id=message.document.file_id,
        file_name=file_name,
        file_bytes=content,
    )

    await message.answer("Файл отправлен на сервер!")
