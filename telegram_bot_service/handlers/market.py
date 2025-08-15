import aiogram
import aiogram.filters
import aiogram.utils.keyboard
import callback
import content.config
import content.user
import keyboards
import logic.list_menu
import logic.menu
import rabbit

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
        aiogram.F.second_prefix == "market",
    )
)
async def product_handler(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.CellCallback,
):
    pass
