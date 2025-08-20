import asyncio
import functools
from typing import Any, Callable

import celery


class AsyncCelery(celery.Celery):
    def __init__(self, *args, broker_instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._broker_instance = broker_instance
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def async_task(self, name: str) -> Callable:
        def decorator(async_func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(async_func)
            def sync_wrapper(*args, **kwargs):
                return self.loop.run_until_complete(
                    async_func(*args, **kwargs)
                )

            return self.task(name=name)(sync_wrapper)

        return decorator

    def async_task_with_broker(self, name: str) -> Callable:
        if self._broker_instance is None:
            raise ValueError("Broker instance is not set for AsyncCelery")

        def decorator(async_func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(async_func)
            def sync_wrapper(*args, **kwargs):
                async def runner():
                    broker = self._broker_instance
                    if hasattr(broker, "__aenter__"):
                        async with broker:
                            return await async_func(*args, **kwargs)
                    else:
                        return await async_func(*args, **kwargs)

                return self.loop.run_until_complete(runner())

            return self.task(name=name)(sync_wrapper)

        return decorator
