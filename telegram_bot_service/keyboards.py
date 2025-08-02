import aiogram.types

import schemas.user
import callback


def build_referrals_keyboard(
    data: schemas.user.ReferralCommandData,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for ref in data.referrals:
        button = aiogram.types.InlineKeyboardButton(
            text=f"👤 {ref.username}",
            callback_data=callback.ReferralCallback(
                action="open", user_id=ref.user_id
            ).pack(),
        )
        inline_keyboard.append([button])
    pagination_row = []
    if data.now_page > 0:
        pagination_row.append(
            aiogram.types.InlineKeyboardButton(
                text="◀ Назад",
                callback_data=callback.ReferralPageCallback(
                    user_id=data.user_id,
                    page=data.now_page - 1,
                    message_id=data.message_id,
                ).pack(),
            )
        )
    if data.now_page < data.max_page - 1:
        pagination_row.append(
            aiogram.types.InlineKeyboardButton(
                text="Вперёд ▶",
                callback_data=callback.ReferralPageCallback(
                    user_id=data.user_id,
                    page=data.now_page + 1,
                    message_id=data.message_id,
                ).pack(),
            )
        )
    if pagination_row:
        inline_keyboard.append(pagination_row)
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
