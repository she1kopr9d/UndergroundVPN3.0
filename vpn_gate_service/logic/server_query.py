import uuid
import httpx

import schemas.config
import schemas.servers
import schemas.telegram

import database.io.server
import database.io.config
import database.io.telegram_user


async def create_config(
    create_data: schemas.config.CreateConfig,
    server_data: schemas.servers.ServerPublicInfo,
) -> str:
    user_data = await database.io.telegram_user.get_telegram_user_data(
        user_id=create_data.user_id,
    )
    user_uuid = uuid.uuid4()
    payload = {
        "email": str(user_uuid) + "@user.id",
        "uuid": str(user_uuid),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{server_data.ip}:{server_data.port}/user/add",
            json=payload,
            timeout=10.0,
        )

    data = response.json()

    if data["status"] != "ok":
        raise RuntimeError("Ошибка при создании конфигурации")

    server_id = database.io.server.get_server_id_by_name(server_data.name)

    await database.io.config.create_config(
        uuid=str(user_uuid),
        config=data["config"],
        server_id=server_id,
        user_data=user_data,
    )

    return data["config"]
