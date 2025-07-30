import sys
import asyncio
import logging

import aiogram

import deps
import rabbit

import handlers.user
import handlers.admin

import subscribers.user  # noqa
import subscribers.admin  # noqa

dp = aiogram.Dispatcher()
logging.basicConfig(level=logging.INFO)


async def main():
    mode = sys.argv[1]
    print("Starting bot")
    if mode == "bot":
        dp.include_router(handlers.user.router)
        dp.include_router(handlers.admin.router)
        async with rabbit.broker:
            await rabbit.broker.start()
            await dp.start_polling(deps.bot)
    elif mode == "broker":
        await rabbit.broker.start()
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
