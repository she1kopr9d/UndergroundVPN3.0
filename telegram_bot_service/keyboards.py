import aiogram.types
import callback
import schemas.base
import schemas.config
import schemas.deposite
import schemas.payments
import schemas.user
import schemas.moderator


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
    paggination_row = get_paggination_row(
        data,
        data.user_id,
        data.message_id,
        "ref",
    )
    if paggination_row:
        inline_keyboard.append(paggination_row)
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
    paggination_row = get_paggination_row(
        data,
        data.user_id,
        data.message_id,
        "conf",
    )
    if paggination_row:
        inline_keyboard.append(paggination_row)
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_payments_keyboard(
    data: schemas.payments.PaymentPageANSW,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    prefix = "pay_list"
    for pay in data.payments:
        button = aiogram.types.InlineKeyboardButton(
            text=f"{pay.payment_id} {pay.payment_method}",
            callback_data=callback.CellCallback(
                action="open",
                user_id=data.user_id,
                message_id=data.message_id,
                page=data.now_page,
                external_id=pay.payment_id,
                second_prefix=prefix,
            ).pack(),
        )
        inline_keyboard.append([button])
    paggination_row = get_paggination_row(
        data,
        data.user_id,
        data.message_id,
        prefix,
    )
    if paggination_row:
        inline_keyboard.append(paggination_row)
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_config_button(
    text: str,
    action: str,
    config_id: int,
    user_id: int,
    now_page: int,
    message_id: int,
):
    return aiogram.types.InlineKeyboardButton(
        text=text,
        callback_data=callback.ConfigCallback(
            action=action,
            config_id=config_id,
            user_id=user_id,
            page=now_page,
            message_id=message_id,
        ).pack(),
    )


def build_config_info_keyboard(
    data: schemas.config.ConfigInfoANSW,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for text, action in [
        ("Удалить", "delete_1"),
        ("Назад", "back"),
    ]:
        inline_keyboard.append(
            [
                build_config_button(
                    text,
                    action,
                    data.config_id,
                    data.user_id,
                    data.now_page,
                    data.message_id,
                )
            ]
        )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_delete_accept_keyboard(
    data: callback.ConfigCallback,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for text, action in [("Отмена", "open"), ("Удалить", "delete_2")]:
        inline_keyboard.append(
            [
                build_config_button(
                    text,
                    action,
                    data.config_id,
                    data.user_id,
                    data.page,
                    data.message_id,
                )
            ]
        )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_deposit_button(
    user_id: int,
    name: str,
    method: str,
) -> aiogram.types.InlineKeyboardButton:
    return aiogram.types.InlineKeyboardButton(
        text=name,
        callback_data=callback.DepositCallback(
            user_id=user_id,
            deposit_method=method,
        ).pack(),
    )


def build_deposit_keyboard(
    user_id: int,
    payment_methods: list,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for method in payment_methods:
        inline_keyboard.append(
            [
                build_deposit_button(
                    user_id=user_id,
                    name=method["title"],
                    method=method["method"],
                )
            ]
        )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_payment_accept_keyboard(
    data: schemas.deposite.DepositeCreateANSW,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(
                text="Подтвердить оплату",
                callback_data=callback.DepositAcceptCallback(
                    action="accept",
                    user_id=data.user_id,
                    message_id=data.message_id,
                    payment_id=data.payment_id,
                ).pack(),
            )
        ],
        [
            aiogram.types.InlineKeyboardButton(
                text="Отменить",
                callback_data=callback.DepositAcceptCallback(
                    action="cancel",
                    user_id=data.user_id,
                    message_id=data.message_id,
                    payment_id=data.payment_id,
                ).pack(),
            )
        ],
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_moderator_accept_keyboard(
    data: schemas.moderator.PaymentModerCellData,
    new_message_id: int,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(
                text="Подтвердить платеж",
                callback_data=callback.DepositAcceptCallback(
                    action="accept_1_moder",
                    user_id=data.user_id,
                    message_id=new_message_id,
                    payment_id=data.payment.payment_id,
                ).pack(),
            )
        ],
        [
            aiogram.types.InlineKeyboardButton(
                text="Отказать",
                callback_data=callback.DepositAcceptCallback(
                    action="cancel_1_moder",
                    user_id=data.user_id,
                    message_id=new_message_id,
                    payment_id=data.payment.payment_id,
                ).pack(),
            )
        ],
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
