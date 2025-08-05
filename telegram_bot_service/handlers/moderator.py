import aiogram
import aiogram.types
import aiogram.filters
import aiogram.fsm.context

import filters.is_moderator

# import config
# import rabbit
# import keyboards
# import logic.payments
# import callback
# import states
import logic.list_menu


router: aiogram.Router = aiogram.Router()
router.message.filter(filters.is_moderator.IsModeratorFilter())


@router.message(aiogram.filters.Command("pay_list"))
async def pay_list_handler(message: aiogram.types.Message):
    await logic.list_menu.load_page_handler(
        message,
        "pay_list_command",
    )
