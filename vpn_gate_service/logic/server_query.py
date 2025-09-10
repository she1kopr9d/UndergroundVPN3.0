import uuid

import config
import database.io.base
import database.io.config
import database.io.server
import database.io.telegram_user
import database.models
import httpx
import schemas.config
import schemas.servers
import schemas.telegram
import re


def clean_string(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9-]", "", s)


def get_user_email(user_name: str) -> str:
    return f"{clean_string(user_name)}"


async def create_config_url(
    user_uuid: str,
    user_email: str,
    server_data: schemas.servers.ServerPublicInfo,
    server_public_key: str,
) -> str:
    vless_link = (
        "vless://"
        f"{user_uuid}@{server_data.vpn_ip}:{server_data.vpn_port}"
        f"?encryption={config.xray.ENCRYPTION}"
        "&flow=xtls-rprx-vision"
        f"&security={config.xray.SECURITY}"
        f"&sni={config.xray.HOST}"
        f"&fp={config.xray.FINGERPRINT}"
        f"&pbk={server_public_key}"
        f"&sid={config.xray.SHORTID}"
        f"&type={config.xray.NET_TYPE}#{user_email}"
    )
    return vless_link


async def create_config(
    create_data: schemas.config.CreateConfig,
    server_data: schemas.servers.ServerPublicInfo,
    subscription_id: int | None = None,
) -> str:
    user_data = await database.io.telegram_user.get_telegram_user_data(
        user_id=create_data.user_id,
    )
    user_uuid = uuid.uuid4()
    user_email = get_user_email(create_data.config_name)
    secret_key = database.io.server.get_secret_key_by_name(server_data.name)
    payload = {
        "email": user_email,
        "uuid": str(user_uuid),
        "secret_key": secret_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{server_data.ip}:{server_data.port}/user/add",
            json=payload,
            timeout=10.0,
        )
    data = response.json()
    valid_status = ["exists", "created"]
    if data["status"] not in valid_status:
        raise RuntimeError("cell server drop error")
    server_id = database.io.server.get_server_id_by_name(server_data.name)
    server_conf_obj: database.models.ServerConfig = (
        await database.io.base.get_object_by_field(
            field=database.models.ServerConfig.server_id,
            value=server_id,
            object_class=database.models.ServerConfig,
        )
    )
    config_url = await create_config_url(
        user_uuid,
        user_email,
        server_data,
        server_conf_obj.public_key
    )
    config_obj: database.models.Config = (
        await database.io.config.create_config(
            name=create_data.config_name,
            uuid=str(user_uuid),
            config=config_url,
            server_id=server_id,
            user_data=user_data,
        )
    )
    await database.io.server.add_user_in_config(
        str(user_uuid),
        user_email,
        server_id,
        lambda temp_uuid, temp_email: {
            "email": temp_email,
            "id": temp_uuid,
            "flow": "xtls-rprx-vision",
            "level": 0,
        },
        lambda temp_config_data, temp_client_data: (
            temp_config_data["inbounds"][0]["settings"]["clients"].append(
                temp_client_data
            )
        ),
    )
    if subscription_id is not None:
        await database.io.base.update_field(
            object_class=database.models.Subscription,
            search_field=database.models.Subscription.id,
            search_value=subscription_id,
            update_list={
                "external_id": config_obj.id,
            },
        )
    return config_url


async def delete_config(
    data: schemas.config.ConfigDelete,
    server_data: schemas.servers.ServerPublicInfo,
    config_obj: database.models.Config,
):
    user_email = get_user_email(config_obj.name)
    secret_key = database.io.server.get_secret_key_by_name(server_data.name)
    payload = {
        "email": user_email,
        "uuid": config_obj.uuid,
        "secret_key": secret_key,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{server_data.ip}:{server_data.port}/user/remove",
            json=payload,
            timeout=10.0,
        )
    data = response.json()
    valid_status = ["not exists", "deleted"]
    if data["status"] not in valid_status:
        raise RuntimeError("cell server drop error")
    server_id = database.io.server.get_server_id_by_name(server_data.name)
    await database.io.server.delete_user_from_config(
        config_obj.uuid,
        server_id,
        lambda temp_config_data, temp_uuid: (
            [
                client
                for client in temp_config_data["inbounds"][0]["settings"][
                    "clients"
                ]
                if client["id"] != temp_uuid
            ]
        ),
    )
    await database.io.base.delete_object_by_id(
        config_obj.id,
        database.models.Config,
    )
