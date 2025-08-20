import aiogram
import aiogram.filters
import aiogram.fsm.context
import aiogram.types
import filters.is_admin
import rabbit
import services.news.callbackdata
import services.news.keyboards
import services.news.states

router = aiogram.Router()
router.message.filter(filters.is_admin.IsAdminFilter())


@router.message(aiogram.filters.Command("news"))
async def cmd_news(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.set_state(services.news.states.NewsStates.get_news)
    await message.answer(
        "Пришлите сообщение с новостью (может быть с картинкой или без)"
    )


@router.message(services.news.states.NewsStates.get_news)
async def get_news_message(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(message_id=message.message_id)

    await message.answer(
        "Вы хотите отправить эту новость пользователям?",
        reply_markup=services.news.keyboards.get_news_keyboard(),
    )


@router.callback_query(
    services.news.callbackdata.NewsAction.filter(aiogram.F.action == "no")
)
async def cancel_news(
    callback: aiogram.types.CallbackQuery,
    state: aiogram.fsm.context.FSMContext,
):
    await state.clear()
    await callback.message.edit_text("Отправка новости отменена ❌")


@router.callback_query(
    services.news.callbackdata.NewsAction.filter(aiogram.F.action == "yes")
)
async def confirm_news(
    callback: aiogram.types.CallbackQuery,
    state: aiogram.fsm.context.FSMContext,
    bot: aiogram.Bot,
):
    data = await state.get_data()
    msg_id = data.get("message_id")
    chat_id = callback.message.chat.id
    msg = await bot.forward_message(
        chat_id=chat_id, from_chat_id=chat_id, message_id=msg_id
    )
    photo = None
    if msg.photo:
        file_id = msg.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_bytes = await bot.download_file(file.file_path)
        photo = file_bytes.read().decode("latin-1")
    text = msg.text or msg.caption if (msg.text or msg.caption) else None
    news_dict = {
        "photo": photo,
        "text": text,
    }
    await rabbit.broker.publish(
        news_dict,
        queue="send_new_news",
    )
    await callback.message.edit_text("Новость подготовлена")
    await state.clear()
