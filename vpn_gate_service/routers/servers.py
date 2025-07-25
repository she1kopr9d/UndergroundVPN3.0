import fastapi
import typing
import time
import asyncio
import faststream.rabbit.fastapi

import config
import schemas.servers
import database.io.server


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


active_servers: dict[str, tuple[schemas.servers.ServerPublicInfo, float]] = {}

CLEANUP_INTERVAL = 30
SERVER_TIMEOUT = 60


@router.post("/server/auth")
async def server_auth(request: schemas.servers.ServerAuth):
    if not database.io.server.server_exists(request):
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid secret key"
        )
    public_info = schemas.servers.ServerPublicInfo(
        name=request.name,
        ip=request.ip,
        port=request.port,
        api_version=request.api_version,
    )
    active_servers[request.name] = (public_info, time.time())
    await router.broker.publish(
        {
            "user_id": 798030433,
            "server_name": request.name,
            "server_ip": request.ip,
            "server_port": request.port,
            "status": "start"
        },
        queue="notification_auth_server",
    )
    return {"status": "ok", "message": "Сервер авторизован"}


@router.post("/server/handshake")
async def server_handshake(request: schemas.servers.ServerAuth):
    if request.name not in active_servers:
        raise fastapi.HTTPException(
            status_code=403, detail="Сервер не авторизован"
        )
    public_info = schemas.servers.ServerPublicInfo(
        name=request.name,
        ip=request.ip,
        port=request.port,
        api_version=request.api_version,
    )
    active_servers[request.name] = (public_info, time.time())
    return {"status": "ok", "message": "Handshake успешен"}


@router.get(
    "/servers/active",
    response_model=typing.List[schemas.servers.ServerPublicInfo],
)
async def get_active_servers():
    return [info for info, _ in active_servers.values()]


async def cleanup_inactive_servers():
    while True:
        current_time = time.time()
        for name, (info, last_handshake) in list(active_servers.items()):
            if current_time - last_handshake > SERVER_TIMEOUT:
                del active_servers[name]
                await router.broker.publish(
                    {
                        "user_id": 798030433,
                        "server_name": info.name,
                        "server_ip": info.ip,
                        "server_port": info.port,
                        "status": "stop"
                    },
                    queue="notification_auth_server",
                )
        await asyncio.sleep(CLEANUP_INTERVAL)


@router.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_inactive_servers())
