import aiogram
import aiogram.fsm.context
import aiogram.types
import callback
import logic.list_menu
import logic.menu
import content.user

router: aiogram.Router = aiogram.Router()


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "main",
    )
)
async def main_menu_back(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
    bot: aiogram.Bot,
    state: aiogram.fsm.context.FSMContext,
):
    await state.clear()
    await logic.menu.main_menu(
        bot,
        chat_id=callback_data.user_id,
        message_id=callback_data.message_id,
    )


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "prof",
    )
)
async def profile_menu(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
    bot: aiogram.Bot,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(message_id=callback_data.message_id)
    await logic.menu.profile_menu_request(
        user_id=callback_data.user_id,
    )


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "ref",
    )
)
async def referral_menu(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
):
    await logic.list_menu.publish_list_menu(
        queue="ref_command",
        user_id=callback_data.user_id,
        message_id=callback_data.message_id,
    )


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "conf",
    )
)
async def config_menu(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
):
    await logic.list_menu.publish_list_menu(
        queue="conf_command",
        user_id=callback_data.user_id,
        message_id=callback_data.message_id,
    )


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "dep",
    )
)
async def deposit_menu(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
    bot: aiogram.Bot,
    state: aiogram.fsm.context.FSMContext,
):
    await state.clear()
    await logic.menu.deposit_menu(
        user_id=callback_data.user_id,
        message_id=callback_data.message_id,
        bot=bot,
    )


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "app",
    )
)
async def app_menu(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
    bot: aiogram.Bot,
    state: aiogram.fsm.context.FSMContext,
):
    await state.clear()
    await query.message.answer(
        text=content.user.APP_COMMAND(),
        parse_mode="HTML",
    )


@router.callback_query(
    callback.MainMenuCallBack.filter(
        aiogram.F.action == "guide",
    )
)
async def guide_menu(
    query: aiogram.types.CallbackQuery,
    callback_data: callback.MainMenuCallBack,
    bot: aiogram.Bot,
    state: aiogram.fsm.context.FSMContext,
):
    await state.clear()
    await query.message.answer(
        text=content.user.GUIDE_COMMAND(),
        parse_mode="HTML",
    )