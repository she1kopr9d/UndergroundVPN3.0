import aiogram
import aiogram.fsm.context
import aiogram.fsm.storage.base
import aiogram.fsm.storage.memory
import config

dp = aiogram.Dispatcher(storage=aiogram.fsm.storage.memory.MemoryStorage())
bot = aiogram.Bot(token=config.settings.TELEGRAM_TOKEN)


async def get_bot() -> aiogram.Bot:
    return bot


async def get_state(user_id: int) -> aiogram.fsm.context.FSMContext:
    state = aiogram.fsm.context.FSMContext(
        storage=dp.storage,
        key=aiogram.fsm.storage.base.StorageKey(
            bot_id=bot.id,
            user_id=user_id,
            chat_id=user_id,
        ),
    )
    return state
