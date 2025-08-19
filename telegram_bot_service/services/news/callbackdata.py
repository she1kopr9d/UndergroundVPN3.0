import aiogram.filters.callback_data


class NewsAction(aiogram.filters.callback_data.CallbackData, prefix="news"):
    action: str
