import asyncio
import aiogram

import config
import broker

import handlers.user


bot = aiogram.Bot(token=config.settings.TELEGRAM_TOKEN)
dp = aiogram.Dispatcher()


async def main():
    async with broker.broker_obj:
        dp.include_router(handlers.user.router)
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
