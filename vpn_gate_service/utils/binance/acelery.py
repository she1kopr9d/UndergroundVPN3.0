# import asyncio

# import celery
# from celery import signals
# from functools import wraps
# from typing import Any, Callable


# class Celery(celery.Celery):

#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         super().__init__(*args, **kwargs)
#         self.functions: dict[str, Callable[..., Any]] = {}
#         self.loop = asyncio.get_event_loop()

#     def connect(self, *_: Any, **__: Any) -> None:
#         self.loop.run_until_complete(connect_to_store())

#     def disconnect(self, *_: Any, **__: Any) -> None:
#         self.loop.run_until_complete(disconnect_from_store())

#     def task(
#         self,
#         task: Callable[..., Awaitable[T]] | None = None,
#         **opts: Any,
#     ) -> Callable:
#         # декоратор от celery
#         create_task = super().task

#         def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., T]:
#             @create_task(**opts)  # регистрируем задачу
#             @wraps(func)
#             def wrapper(*args: Any, loop: AbstractEventLoop | None = None, **kwargs: Any) -> T:
#                 # для случаев, когда очень хочется выполнить задачу сразу (без apply_async)
#                 loop = loop or self.loop

#                 # выполняем асинхронную функцию в цикле событий
#                 return loop.run_until_complete(func(*args, **kwargs))
            
#             # запоминаем функцию для удобства тестирования
#             self.functions[wrapper.name] = func

#             return wrapper

#         if task:
#             return decorator(task)

#         return decorator
