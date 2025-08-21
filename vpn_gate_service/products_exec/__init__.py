from products_exec.real.vpn_30_days import VPN_30_DAYS
from products_exec.real.vpn_90_days import VPN_90_DAYS

__all__ = ["VPN_30_DAYS", "VPN_90_DAYS"]

exec_list = {
    "vpn_30_day": VPN_30_DAYS,
    "vpn_90_day": VPN_90_DAYS,
}
