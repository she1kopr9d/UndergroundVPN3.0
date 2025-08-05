import aiogram
import aiogram.filters
import aiogram.fsm.context
import aiogram.types
import callback
import rabbit
import filters.is_moderator
import logic.list_menu

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
