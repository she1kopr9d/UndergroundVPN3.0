import aiogram.filters.callback_data


class PageCallback(aiogram.filters.callback_data.CallbackData, prefix="page"):
    user_id: int
    page: int
    message_id: int
    move: str


class ReferralCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="ref",
):
    action: str
    user_id: int
    referral_user_id: int
    page: int
    message_id: int


class ConfigCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="conf",
):
    action: str
    user_id: int
    message_id: int
    config_id: int
    page: int


class DepositCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="dep",
):
    user_id: int
    deposit_method: str
