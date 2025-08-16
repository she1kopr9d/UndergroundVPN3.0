from tasks.example import (
    periodic_task,
    test_task,
)
from tasks.config import (
    create_config_task,
)
from tasks.products import (
    exec_vpn_30_days,
    remove_vpn_30_days,
)


__all__ = [
    "periodic_task",
    "test_task",
    "create_config_task",
    "exec_vpn_30_days",
    "remove_vpn_30_days",
]


def get_func_complex(exec, remove) -> dict:
    return {
        "exec": exec,
        "remove": remove,
    }


exec_list = {
    "vpn_30_days": get_func_complex(
        exec_vpn_30_days,
        remove_vpn_30_days,
    )
}
