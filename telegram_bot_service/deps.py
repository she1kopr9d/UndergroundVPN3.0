import aiogram
import config

bot = aiogram.Bot(token=config.settings.TELEGRAM_TOKEN)


async def get_bot() -> aiogram.Bot:
    return bot
