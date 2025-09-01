import products_exec.abs.vpn
import database.models
import database.io.base


class VPN_TRIAL_VERSION(products_exec.abs.vpn.VPNProduct):
    async def check(self, user_id: int) -> bool:
        user: database.models.TelegramUser = (
            await database.io.base.get_object_by_field(
                field=database.models.TelegramUser.telegram_id,
                value=user_id,
                object_class=database.models.TelegramUser,
            )
        )
        if not user.is_trial:
            await self.broker.publish(
                {
                    "user_id": user_id,
                    "text": (
                        "Вы уже использовали пробную версию, "
                        "оформите платную подписку для дальнейшего "
                        "использования сервиса."
                    ),
                    "photo": None,
                },
                queue="send_telegram_message",
            )
            return False
        else:
            return await super().check(user_id)

    async def create(self, user_id, subscription_id) -> None:
        await database.io.base.update_field(
            search_field=database.models.TelegramUser.telegram_id,
            search_value=user_id,
            object_class=database.models.TelegramUser,
            update_list={
                "is_trial": False,
            }
        )
        return await super().create(user_id, subscription_id)

    async def remove(self, user_id, subscription_id) -> None:
        return await super().remove(user_id, subscription_id)

    async def update(self, user_id, subscription_id) -> bool:
        await self.remove(user_id, subscription_id)
        await self.broker.publish(
            {
                "user_id": user_id,
                "text": (
                    "Пробная версия закончилась, для дальнейшего "
                    "использования сервиса оформите платную подписку."
                ),
                "photo": None,
            },
            queue="send_telegram_message",
        )
        return False
