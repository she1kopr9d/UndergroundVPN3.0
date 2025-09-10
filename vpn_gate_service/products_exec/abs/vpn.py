import random
import re

import database.io.base
import database.models
import logic.server_query
import logic.server_session
import database.io.server
import products_exec.abs.base
import rabbit
import schemas.config
import schemas.servers
import tasks.config


def clean_string(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9-]", "", s)


class VPNProduct(products_exec.abs.base.Product):
    async def check(self, user_id: int) -> bool:
        if not logic.server_session.active_servers:
            await self.broker.publish(
                {
                    "user_id": user_id,
                    "text": (
                        "🚫 Сервера для выдачи переполнены. "
                        "Обратитесь в поддержку или "
                        "попробуйте в другой раз."
                    ),
                    "photo": None,
                },
                queue="send_telegram_message",
            )
            return False
        return await super().check(user_id)

    async def create(self, user_id, subscription_id) -> None:
        user: database.models.TelegramUser = (
            await database.io.base.get_object_by_field(
                field=database.models.TelegramUser.telegram_id,
                value=user_id,
                object_class=database.models.TelegramUser,
            )
        )
        config_name = (
            f"{clean_string(user.username)}-{random.randint(0, 0xFFFF):04X}"
        )
        servers = logic.server_session.get_active_servers()
        servers_name = [server.name for server in servers]
        server_name = await database.io.server.get_low_server_id(servers_name)
        server = logic.server_session.get_active_server(server_name)
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

    async def remove(self, user_id: int, subscription_id: int) -> None:
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

    async def update(self, user_id: int, subscription_id: int) -> bool:
        return await super().update(user_id, subscription_id)
