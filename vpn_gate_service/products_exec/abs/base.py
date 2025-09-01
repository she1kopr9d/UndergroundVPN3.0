import faststream.rabbit.fastapi


class Product:
    broker: faststream.rabbit.fastapi.RabbitBroker = None

    def __init__(
        self,
        broker: faststream.rabbit.fastapi.RabbitBroker = None,
    ):
        self.broker = broker

    async def check(self, user_id: int) -> bool:
        return True

    async def create(self, user_id: int, subscription_id: int) -> None:
        pass

    async def remove(self, user_id: int, subscription_id: int) -> None:
        pass

    async def update(self, user_id: int, subscription_id: int) -> bool:
        return True
