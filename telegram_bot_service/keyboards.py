import aiogram.types
import callback
import schemas.base
import schemas.config
import schemas.deposite
import schemas.moderator
import schemas.payments
import schemas.product
import schemas.user


def build_main_menu_button(
    text: str,
    action: str,
    user_id: int,
    message_id: int,
) -> aiogram.types.InlineKeyboardButton:
    return aiogram.types.InlineKeyboardButton(
        text=text,
        callback_data=callback.MainMenuCallBack(
            action=action,
            user_id=user_id,
            message_id=message_id,
        ).pack(),
    )


def build_back_to_main_menu_button(
    user_id: int,
    message_id: int,
) -> aiogram.types.InlineKeyboardButton:
    return build_main_menu_button(
        text="В меню",
        action="main",
        user_id=user_id,
        message_id=message_id,
    )


def build_back_to_main_menu_keyboard(
    user_id: int,
    message_id: int,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [[build_back_to_main_menu_button(user_id, message_id)]]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


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
    if data.referrals is not None:
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
    inline_keyboard.append(
        [
            build_back_to_main_menu_button(
                user_id=data.user_id,
                message_id=data.message_id,
            )
        ]
    )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_configs_keyboard(
    data: schemas.config.ConfigPageANSW,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    if data.configs is not None:
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
    inline_keyboard.append(
        [
            build_back_to_main_menu_button(
                user_id=data.user_id,
                message_id=data.message_id,
            )
        ]
    )
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
    for text, action in [
        ("Отменять", "open"),
        ("Удалить", "delete_2"),
    ]:
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


def build_sub_config_info_keyboard(
    data: schemas.config.ConfigInfoANSW,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for text, action in [
        ("Отменить подписку", "cancel_1"),
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


def build_cancel_accept_keyboard(
    data: callback.ConfigCallback,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for text, action in [
        ("Не отменять", "open"),
        ("Точно отменить", "cancel_2"),
    ]:
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


def build_resub_config_info_keyboard(
    data: schemas.config.ConfigInfoANSW,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for text, action in [
        ("Возобновить подписку", "resub_1"),
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


def build_resub_accept_keyboard(
    data: callback.ConfigCallback,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    for text, action in [
        ("Не возобновлять", "open"),
        ("Возобновить", "resub_2"),
    ]:
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
    message_id: int,
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
    inline_keyboard.append(
        [
            build_back_to_main_menu_button(
                user_id=user_id,
                message_id=message_id,
            )
        ]
    )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_payment_accept_button(
    text: str,
    action: str,
    data: schemas.deposite.DepositeCreateANSW,
    link: str | None = None,
) -> aiogram.types.InlineKeyboardButton:
    kwargs = dict()
    if link is not None:
        kwargs.update(url=link)
    else:
        kwargs.update(
            callback_data=callback.DepositAcceptCallback(
                action=action,
                user_id=data.user_id,
                message_id=data.message_id,
                payment_id=data.payment_id,
            ).pack()
        )
    return aiogram.types.InlineKeyboardButton(
        text=text,
        **kwargs,
    )


def build_payment_accept_keyboard(
    data: schemas.deposite.DepositeCreateANSW,
    link: str | None = None,
) -> aiogram.types.InlineKeyboardMarkup:
    accept_button = None
    if data.method == "telegram_star":
        accept_button = build_payment_accept_button(
            f"Оплатить {data.amount} ⭐️",
            None,
            data,
            link,
        )
    else:
        accept_button = build_payment_accept_button(
            "Подтвердить оплату",
            "accept",
            data,
        )
    cancel_button = build_payment_accept_button(
        "Отменить",
        "cancel",
        data,
    )
    inline_keyboard = [[accept_button], [cancel_button]]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_moderator_accept_button(
    text: str,
    action: str,
    data: schemas.moderator.PaymentModerCellData,
    new_message_id: int,
) -> aiogram.types.InlineKeyboardButton:
    return aiogram.types.InlineKeyboardButton(
        text=text,
        callback_data=callback.DepositAcceptCallback(
            action=action,
            user_id=data.user_id,
            message_id=new_message_id,
            payment_id=data.payment.payment_id,
        ).pack(),
    )


def build_moderator_accept_button_callback(
    text: str,
    action: str,
    data: callback.DepositAcceptCallback,
) -> aiogram.types.InlineKeyboardButton:
    return aiogram.types.InlineKeyboardButton(
        text=text,
        callback_data=callback.DepositAcceptCallback(
            action=action,
            user_id=data.user_id,
            message_id=data.message_id,
            payment_id=data.payment_id,
        ).pack(),
    )


def build_moderator_accept_keyboard(
    data: schemas.moderator.PaymentModerCellData,
    new_message_id: int,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [build_moderator_accept_button(text, action, data, new_message_id)]
        for text, action in [
            ("Подтвердить платеж", "accept_1_moder"),
            ("Отказать", "cancel_1_moder"),
        ]
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_moderator_accept_2_keyboard(
    data: callback.DepositAcceptCallback,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [build_moderator_accept_button_callback(text, action, data)]
        for text, action in [
            ("Назад", "back_moder"),
            ("Точно подтвердить", "accept_2_moder"),
        ]
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_moderator_cancel_2_keyboard(
    data: callback.DepositAcceptCallback,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [build_moderator_accept_button_callback(text, action, data)]
        for text, action in [
            ("Точно отказать", "cancel_2_moder"),
            ("Назад", "back_moder"),
        ]
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_moderator_back_keyboard(
    data: callback.DepositAcceptCallback,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [build_moderator_accept_button_callback(text, action, data)]
        for text, action in [
            ("Подтвердить платеж", "accept_1_moder"),
            ("Отказать", "cancel_1_moder"),
        ]
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_main_menu_keyboard(
    user_id: int,
    message_id: int,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [build_main_menu_button(text, action, user_id, message_id)]
        for text, action in [
            ("Профиль", "prof"),
            ("Рефералы", "ref"),
            ("Пополнить баланс", "dep"),
            ("Конфиги", "conf"),
            ("К покупкам", "buy"),
            ("Cсылки на приложения", "app"),
            ("Гайд", "guide"),
        ]
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_back_to_menu_button(
    user_id: int,
    message_id: int,
    action: str,
) -> aiogram.types.InlineKeyboardButton:
    return build_main_menu_button(
        text="Назад",
        action=action,
        user_id=user_id,
        message_id=message_id,
    )


def build_back_to_menu_keyboard(
    user_id: int,
    message_id: int,
    action: str,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = [
        [build_back_to_menu_button(user_id, message_id, action)]
    ]
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_market_list_keyboard(
    user_id: int,
    message_id: int,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    inline_keyboard.append(
        [
            aiogram.types.InlineKeyboardButton(
                text="Подписка на открытый ВПН (30 дней) - 1 устройство",
                callback_data=callback.MarketCallback(
                    user_id=user_id,
                    message_id=message_id,
                    action="",
                ),
            )
        ]
    )
    inline_keyboard.append(
        [build_back_to_main_menu_button(user_id, message_id)]
    )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_market_keyboard(
    data: schemas.product.ProductListData,
) -> aiogram.types.InlineKeyboardMarkup:
    inline_keyboard = []
    prefix = "market"
    for product in data.products:
        button = aiogram.types.InlineKeyboardButton(
            text=f"{product.product_name}",
            callback_data=callback.CellCallback(
                action="open",
                user_id=data.user_id,
                message_id=data.message_id,
                page=data.now_page,
                external_id=product.product_id,
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
    inline_keyboard.append(
        [build_back_to_main_menu_button(data.user_id, data.message_id)]
    )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_product_info_keyboard(
    data: schemas.product.ProductView,
):
    inline_keyboard = []
    inline_keyboard.append(
        [
            aiogram.types.InlineKeyboardButton(
                text="Купить",
                callback_data=callback.CellCallback(
                    action="buy_1",
                    user_id=data.user_id,
                    message_id=data.message_id,
                    page=data.page,
                    external_id=data.product_id,
                    second_prefix="market",
                ).pack(),
            )
        ]
    )
    inline_keyboard.append(
        [build_main_menu_button("Назад", "buy", data.user_id, data.message_id)]
    )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def build_product_accept_buy_keyboard(
    data: callback.CellCallback,
):
    inline_keyboard = []
    inline_keyboard.append(
        [
            aiogram.types.InlineKeyboardButton(
                text="Назад",
                callback_data=callback.CellCallback(
                    action="open",
                    user_id=data.user_id,
                    message_id=data.message_id,
                    page=data.page,
                    external_id=data.external_id,
                    second_prefix=data.second_prefix,
                ).pack(),
            )
        ]
    )
    inline_keyboard.append(
        [
            aiogram.types.InlineKeyboardButton(
                text="Подтвердить",
                callback_data=callback.CellCallback(
                    action="buy_2",
                    user_id=data.user_id,
                    message_id=data.message_id,
                    page=data.page,
                    external_id=data.external_id,
                    second_prefix=data.second_prefix,
                ).pack(),
            )
        ]
    )
    return aiogram.types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
