import fastapi
import asyncio
import typing
import faststream.rabbit.fastapi

import config
import schemas.servers
import database.io.server
import logic.server_session


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


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
    logic.server_session.register_server(public_info)

    await router.broker.publish(
        {
            "user_id": 798030433,
            "server_name": request.name,
            "server_ip": request.ip,
            "server_port": request.port,
            "status": "start",
        },
        queue="notification_auth_server",
    )
    return {"status": "ok", "message": "Сервер авторизован"}


@router.post("/server/handshake")
async def server_handshake(request: schemas.servers.ServerAuth):
    if not logic.server_session.is_authorized(request.name):
        raise fastapi.HTTPException(
            status_code=403, detail="Сервер не авторизован"
        )

    public_info = schemas.servers.ServerPublicInfo(
        name=request.name,
        ip=request.ip,
        port=request.port,
        api_version=request.api_version,
    )
    logic.server_session.update_handshake(public_info)

    return {"status": "ok", "message": "Handshake успешен"}


@router.get(
    "/servers/active",
    response_model=typing.List[schemas.servers.ServerPublicInfo],
)
async def get_active_servers():
    return logic.server_session.get_active_servers()


@router.get("/server/active")
async def get_all_active_servers():
    return {
        "status": "ok",
        "data": logic.server_session.get_active_servers_dict(),
    }


@router.on_event("startup")
async def startup_event():
    async def notify_stop(info: schemas.servers.ServerPublicInfo):
        await router.broker.publish(
            {
                "user_id": 798030433,
                "server_name": info.name,
                "server_ip": info.ip,
                "server_port": info.port,
                "status": "stop",
            },
            queue="notification_auth_server",
        )

    asyncio.create_task(
        logic.server_session.cleanup_inactive_servers(notify_stop)
    )
