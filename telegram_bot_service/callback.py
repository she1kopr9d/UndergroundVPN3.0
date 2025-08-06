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
    message_id: int
    referral_user_id: int
    page: int


class ConfigCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="conf",
):
    action: str
    user_id: int
    message_id: int
    config_id: int
    page: int


class CellCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="call",
):
    action: str
    user_id: int
    message_id: int
    page: int
    external_id: int
    second_prefix: str


class DepositCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="dep",
):
    user_id: int
    deposit_method: str


class DepositAcceptCallback(
    aiogram.filters.callback_data.CallbackData,
    prefix="dep_a",
):
    user_id: int
    message_id: int
    payment_id: int
    action: str


class MainMenuCallBack(
    aiogram.filters.callback_data.CallbackData,
    prefix="m_menu",
):
    user_id: int
    message_id: int
    action: str
