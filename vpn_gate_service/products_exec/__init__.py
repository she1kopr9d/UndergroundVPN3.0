from products_exec.real.vpn_30_days import VPN_30_DAYS
from products_exec.real.vpn_90_days import VPN_90_DAYS
from products_exec.real.vpn_trial_version import VPN_TRIAL_VERSION

import database.models
import database.io.base

__all__ = ["VPN_30_DAYS", "VPN_90_DAYS"]

exec_list = {
    "vpn_30_day": VPN_30_DAYS,
    "vpn_90_day": VPN_90_DAYS,
    "vpn_trial_version": VPN_TRIAL_VERSION,
}


async def get_exec_class_from_product_id(product_id: int):
    exec_product: database.models.ExecuteProduct = (
        await database.io.base.get_object_by_field(
            field=database.models.ExecuteProduct.product_id,
            value=product_id,
            object_class=database.models.ExecuteProduct,
        )
    )
    return exec_list[exec_product.executor_name]


async def get_exec_from_product_id(product_id: int):
    return await get_exec_class_from_product_id(product_id)()
