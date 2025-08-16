import asyncio
import celery
import functools


class AsyncCelery(celery.Celery):
    def __init__(self, *args, broker_instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._broker_instance = broker_instance

    def async_task(self, name: str):
        """
        Декоратор для асинхронных Celery задач без брокера.
        """

        def decorator(async_func):
            @functools.wraps(async_func)
            def sync_wrapper(*args, **kwargs):
                return asyncio.run(async_func(*args, **kwargs))

            return self.task(name=name)(sync_wrapper)

        return decorator

    def async_task_with_broker(self, name: str):
        """
        Декоратор для асинхронных Celery задач с автоматическим подключением к self._broker_instance.
        """
        if self._broker_instance is None:
            raise ValueError("Broker instance is not set for AsyncCelery")

        def decorator(async_func):
            @functools.wraps(async_func)
            def sync_wrapper(*args, **kwargs):
                async def runner():
                    async with self._broker_instance:
                        return await async_func(*args, **kwargs)

                return asyncio.run(runner())

            return self.task(name=name)(sync_wrapper)

        return decorator
