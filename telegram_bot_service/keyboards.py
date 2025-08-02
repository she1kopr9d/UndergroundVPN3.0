import aiogram.types

import callback
import schemas.base
import schemas.config
import schemas.user


def get_paggination_row(
    data: schemas.base.BasePage,
    user_id: int,
    message_id: int,
    move: str,
):
    pagination_row = []
    if data.now_page > 0:
        pagination_row.append(
            aiogram.types.InlineKeyboardButton(
                text="◀ Назад",
                callback_data=callback.PageCallback(
                    user_id=user_id,
                    page=data.now_page - 1,
                    message_id=message_id,
                    move=move,
                ).pack(),
            )
        )
    if data.now_page < data.max_page - 1:
        pagination_row.append(
            aiogram.types.InlineKeyboardButton(
                text="Вперёд ▶",
                callback_data=callback.PageCallback(
                    user_id=user_id,
                    page=data.now_page + 1,
                    message_id=message_id,
                    move=move,
                ).pack(),
            )
        )
    return pagination_row


def build_referrals_keyboard(
    data: schemas.user.ReferralCommandData,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for ref in data.referrals:
        button = aiogram.types.InlineKeyboardButton(
            text=f"👤 {ref.username}",
            callback_data=callback.ReferralCallback(
                action="open",
                referral_user_id=ref.user_id,
                user_id=data.user_id,
                page=data.now_page,
                message_id=data.message_id,
            ).pack(),
        )
        inline_keyboard.append([button])
    pagination_row = get_paggination_row(
        data,
        data.user_id,
        data.message_id,
        "ref",
    )
    if pagination_row:
        inline_keyboard.append(pagination_row)
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_configs_keyboard(
    data: schemas.config.ConfigPageANSW,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for conf in data.configs:
        button = aiogram.types.InlineKeyboardButton(
            text=f"📄 {conf.config_name}",
            callback_data=callback.ConfigCallback(
                action="open",
                config_id=conf.config_id,
                user_id=data.user_id,
                page=data.now_page,
                message_id=data.message_id,
            ).pack(),
        )
        inline_keyboard.append([button])
    pagination_row = get_paggination_row(
        data,
        data.user_id,
        data.message_id,
        "conf",
    )
    if pagination_row:
        inline_keyboard.append(pagination_row)
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_config_info_keyboard(
    data: schemas.config.ConfigInfoANSW
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for text, action in [
        ("Удалить", "delete_1"),
        ("Назад", "back"),
    ]:
        inline_keyboard.append([
            aiogram.types.InlineKeyboardButton(
                text=text,
                callback_data=callback.ConfigCallback(
                    action=action,
                    config_id=data.config_id,
                    user_id=data.user_id,
                    page=data.now_page,
                    message_id=data.message_id,
                ).pack(),
            )
        ])
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
