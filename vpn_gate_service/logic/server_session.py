import asyncio
import time
from typing import Dict, List, Tuple

import schemas.servers

CLEANUP_INTERVAL = 30
SERVER_TIMEOUT = 60

active_servers: Dict[str, Tuple[schemas.servers.ServerPublicInfo, float]] = {}


def is_authorized(name: str) -> bool:
    return name in active_servers


def register_server(info: schemas.servers.ServerPublicInfo) -> None:
    active_servers[info.name] = (info, time.time())


def update_handshake(info: schemas.servers.ServerPublicInfo) -> None:
    active_servers[info.name] = (info, time.time())


def get_active_servers() -> List[schemas.servers.ServerPublicInfo]:
    return [info for info, _ in active_servers.values()]


def get_active_servers_dict() -> (
    Dict[str, Tuple[schemas.servers.ServerPublicInfo, float]]
):
    return active_servers


def get_active_server(server_name: str):
    return active_servers[server_name][0]


async def cleanup_inactive_servers(publish_callback):
    while True:
        current_time = time.time()
        for name, (info, last_handshake) in list(active_servers.items()):
            if current_time - last_handshake > SERVER_TIMEOUT:
                del active_servers[name]
                await publish_callback(info)
        await asyncio.sleep(CLEANUP_INTERVAL)
