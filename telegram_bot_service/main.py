import sys
import asyncio
import logging

import aiogram
import aiogram.fsm.storage.memory

import deps
import rabbit

import handlers.admin
import handlers.deposit
import handlers.user

import subscribers.user  # noqa
import subscribers.admin  # noqa

dp = aiogram.Dispatcher(storage=aiogram.fsm.storage.memory.MemoryStorage())
logging.basicConfig(level=logging.INFO)


async def main():
    mode = sys.argv[1]
    print("Starting bot")
    if mode == "bot":
        dp.include_router(handlers.admin.router)
        dp.include_router(handlers.deposit.router)
        dp.include_router(handlers.user.router)
        async with rabbit.broker:
            await rabbit.broker.start()
            await dp.start_polling(deps.bot)
    elif mode == "broker":
        await rabbit.broker.start()
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
