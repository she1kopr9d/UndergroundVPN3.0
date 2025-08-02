import aiogram.filters.callback_data


class ReferralCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="ref",
):
    action: str
    user_id: int


class ReferralPageCallback(
    aiogram.filters.callback_data.CallbackData, prefix="ref_page"
):
    user_id: int
    page: int
    message_id: int
