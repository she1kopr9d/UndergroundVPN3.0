import random

import products_exec.abs.base

import schemas.config
import schemas.servers
import logic.server_session
import logic.server_query
import tasks.config

import database.models
import database.io.base

import rabbit


class VPNProduct(products_exec.abs.base.Product):
    async def create(self, user_id, subscription_id):
        user: database.models.TelegramUser = (
            await database.io.base.get_object_by_field(
                field=database.models.TelegramUser.telegram_id,
                value=user_id,
                object_class=database.models.TelegramUser,
            )
        )
        config_name = f"{user.username}-{random.randint(0, 0xFFFF):04X}"
        server = logic.server_session.get_random_server()
        await self.create_config(
            data=schemas.config.CreateConfig(
                user_id=user_id,
                server_name=server.name,
                config_name=config_name,
            ),
            subscription_id=subscription_id,
        )
        return await super().create(user_id, subscription_id)

    async def create_config(
        self,
        data: schemas.config.CreateConfig,
        subscription_id: int,
    ):
        server = logic.server_session.get_active_server(data.server_name)
        tasks.config.create_config_task.delay(
            {
                "user": data.dict(),
                "server": server.dict(),
                "subscription_id": subscription_id,
            }
        )

    async def remove(self, user_id: int, subscription_id: int):
        subscription: database.models.Subscription = (
            await database.io.base.get_object_by_id(
                id=subscription_id,
                object_class=database.models.Subscription,
            )
        )
        await rabbit.broker.publish(
            schemas.config.ConfigDelete(
                user_id=user_id,
                config_id=int(subscription.external_id),
            ).dict(),
            queue="delete_config",
        )
