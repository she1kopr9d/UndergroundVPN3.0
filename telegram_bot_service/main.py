import asyncio
import logging
import sys

import deps
import handlers.admin
import handlers.deposit
import handlers.market
import handlers.menu
import handlers.moderator
import handlers.user
import rabbit
import subscribers.admin  # noqa
import subscribers.moderator  # noqa
import subscribers.user  # noqa

logging.basicConfig(level=logging.INFO)


async def main():
    mode = sys.argv[1]
    print("Starting bot")
    if mode == "bot":
        deps.dp.include_router(handlers.admin.router)
        deps.dp.include_router(handlers.deposit.router)
        deps.dp.include_router(handlers.user.router)
        deps.dp.include_router(handlers.market.router)
        deps.dp.include_router(handlers.moderator.router)
        deps.dp.include_router(handlers.menu.router)
        async with rabbit.broker:
            await rabbit.broker.start()
            await deps.dp.start_polling(deps.bot)
    elif mode == "broker":
        await rabbit.broker.start()
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
