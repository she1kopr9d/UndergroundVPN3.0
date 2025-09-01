import products_exec.abs.vpn


class VPN_90_DAYS(products_exec.abs.vpn.VPNProduct):
    async def create(self, user_id, subscription_id) -> None:
        return await super().create(user_id, subscription_id)

    async def remove(self, user_id, subscription_id) -> None:
        return await super().remove(user_id, subscription_id)
