import aiogram
import aiogram.filters
import callback
import logic.list_menu
import logic.menu
import rabbit
import keyboards

router = aiogram.Router()


@router.message(aiogram.filters.Command("market"))
async def market_handler(message: aiogram.types.Message):
    send_message = await message.answer("Загружаю...")
    await logic.menu.market_menu(
        user_id=message.from_user.id,
        message_id=send_message.message_id,
        bot=message.bot,
    )


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "buy",
    )
)
async def market_callback_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
):
    await logic.list_menu.publish_list_menu(
        queue="market_command",
        user_id=callback_data.user_id,
        message_id=callback_data.message_id,
    )


@router.callback_query(
    callback.CellCallback.filter(
        (aiogram.F.second_prefix == "market") & (aiogram.F.action == "open")
    )
)
async def product_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.CellCallback,
):
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "message_id": callback_data.message_id,
            "product_id": callback_data.external_id,
            "page": callback_data.page,
        },
        queue="product_info",
    )


@router.callback_query(
    callback.CellCallback.filter(
        (aiogram.F.second_prefix == "market") & (aiogram.F.action == "buy_1")
    )
)
async def product_buy_accept_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.CellCallback,
):
    await query.bot.edit_message_reply_markup(
        chat_id=callback_data.user_id,
        message_id=callback_data.message_id,
        reply_markup=keyboards.build_product_accept_buy_keyboard(
            callback_data,
        ),
    )


@router.callback_query(
    callback.CellCallback.filter(
        (aiogram.F.second_prefix == "market") & (aiogram.F.action == "buy_2")
    )
)
async def product_buy_accepted_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.CellCallback,
):
    await query.bot.edit_message_text(
        chat_id=callback_data.user_id,
        message_id=callback_data.message_id,
        text="Производится покупка",
        reply_markup=None,
    )
    await rabbit.broker.publish(
        {
            "user_id": callback_data.user_id,
            "message_id": callback_data.message_id,
            "product_id": callback_data.external_id,
        },
        queue="product_buy",
    )
