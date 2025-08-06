import aiogram
import aiogram.filters
import aiogram.fsm.context
import aiogram.types
import callback
import filters.is_moderator
import keyboards
import logic.list_menu
import rabbit

router: aiogram.Router = aiogram.Router()
router.message.filter(filters.is_moderator.IsModeratorFilter())


@router.message(aiogram.filters.Command("pay_list"))
async def pay_list_handler(message: aiogram.types.Message):
    await logic.list_menu.load_page_handler(
        message,
        "pay_list_command",
    )


@router.callback_query(
    callback.CellCallback.filter(
        aiogram.F.second_prefix == "pay_list",
    )
)
async def pay_cell_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.CellCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "message_id": callback_data.message_id,
            "payment_id": callback_data.external_id,
            "now_page": callback_data.page,
        },
        queue="pay_cell_moder_data",
    )


@router.callback_query(
    callback.DepositAcceptCallback.filter(
        aiogram.F.action == "accept_1_moder",
    )
)
async def moderator_accept_1_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositAcceptCallback,
    bot: aiogram.Bot,
):
    await bot.edit_message_reply_markup(
        chat_id=callback_data.user_id,
        message_id=callback_data.message_id,
        reply_markup=keyboards.build_moderator_accept_2_keyboard(
            callback_data,
        ),
    )


@router.callback_query(
    callback.DepositAcceptCallback.filter(
        aiogram.F.action == "accept_2_moder",
    )
)
async def moderator_accept_2_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositAcceptCallback,
    bot: aiogram.Bot,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "message_id": callback_data.message_id,
            "payment_id": callback_data.payment_id,
        },
        queue="accept_deposit_moder",
    )


@router.callback_query(
    callback.DepositAcceptCallback.filter(
        aiogram.F.action == "cancel_1_moder",
    )
)
async def moderator_cancel_1_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositAcceptCallback,
    bot: aiogram.Bot,
):
    await bot.edit_message_reply_markup(
        chat_id=callback_data.user_id,
        message_id=callback_data.message_id,
        reply_markup=keyboards.build_moderator_cancel_2_keyboard(
            callback_data,
        ),
    )


@router.callback_query(
    callback.DepositAcceptCallback.filter(
        aiogram.F.action == "cancel_2_moder",
    )
)
async def moderator_cancel_2_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositAcceptCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "message_id": callback_data.message_id,
            "payment_id": callback_data.payment_id,
        },
        queue="cancel_deposit_moder",
    )


@router.callback_query(
    callback.DepositAcceptCallback.filter(
        aiogram.F.action == "back_moder",
    )
)
async def moderator_back_moder_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.DepositAcceptCallback,
    bot: aiogram.Bot,
):
    await bot.edit_message_reply_markup(
        chat_id=callback_data.user_id,
        message_id=callback_data.message_id,
        reply_markup=keyboards.build_moderator_back_keyboard(
            callback_data,
        ),
    )
