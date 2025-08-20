import aiogram.types
import aiogram.utils.keyboard
import services.news.callbackdata


def get_news_keyboard() -> aiogram.types.InlineKeyboardMarkup:
    kb = aiogram.utils.keyboard.InlineKeyboardBuilder()
    kb.button(
        text="✅ Да",
        callback_data=services.news.callbackdata.NewsAction(action="yes"),
    )
    kb.button(
        text="❌ Нет",
        callback_data=services.news.callbackdata.NewsAction(action="no"),
    )
    kb.adjust(2)
    return kb.as_markup()
