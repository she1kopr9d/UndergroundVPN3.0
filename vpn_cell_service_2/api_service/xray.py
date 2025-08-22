import json
import pathlib
import shutil
import typing

import config as env_config
import docker
import schemas

# START vpn conteiner space


def load_config() -> dict[str, typing.Any]:
    with open(env_config.settings.config_path, "r") as f:
        return json.load(f)


def restart_xray_container():
    try:
        client = docker.DockerClient(base_url="unix://var/run/docker.sock")
        container = client.containers.get(env_config.settings.XRAY_CONTEINER)
        container.restart()
        print("Xray container restarted successfully.")
    except docker.errors.NotFound:
        print("Xray container not found.")
    except docker.errors.APIError as e:
        print(f"Error restarting Xray container: {e}")


# END vpn conteiner space
# START config space


def save_config(config: dict[str, typing.Any]) -> None:
    path: pathlib.Path = env_config.settings.config_path
    backup_path: pathlib.Path = path.with_suffix(".bak")
    shutil.copy2(path, backup_path)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    restart_xray_container()


def find_inbound(config: dict[str, typing.Any]) -> dict[str, typing.Any]:
    for inbound in config.get("inbounds", []):
        return inbound
    raise ValueError(
        f"Inbound с тегом '{env_config.settings.inbound_tag}' не найден"
    )


def add_user_to_config(
    client_data: dict,
    config: dict[str, typing.Any],
) -> None:
    inbound = find_inbound(config)
    settings = inbound.setdefault("settings", {})
    clients = settings.setdefault("clients", [])

    for client in clients:
        if client.get("email") == client_data.get("email") or client.get(
            "id"
        ) == client_data.get("uuid"):
            return "exists"

    clients.append(
        client_data,
    )
    return "created"


def remove_user_from_config(
    client_data: schemas.ConfigEditInfo,
    config: dict[str, typing.Any],
) -> None:
    inbound = find_inbound(config)
    settings = inbound.get("settings", {})
    clients = settings.get("clients", [])

    updated_clients = []
    for client in clients:
        print(client.get("id"), client_data.uuid)
        print(str(client.get("id")) == str(client_data.uuid))
        if not (str(client.get("id")) == str(client_data.uuid)):
            updated_clients.append(client)

    if len(updated_clients) == len(clients):
        print("test")
        return "not exists"

    settings["clients"] = updated_clients
    save_config(settings)
    return "deleted"


# END config space
# START raw config space


def raw_load_config(data: str) -> None:
    with open(env_config.settings.config_path, "w+") as file:
        file.write(data)


# END raw config space

# def generate_url(email: str, uuid: str) -> str:
#     vless_link = (
#         "vless://"
#         f"{uuid}@{env_config.settings.DOMAIN}:{env_config.settings.VPN_PORT}"
#         f"?encryption={env_config.settings.ENCRYPTION}"
#         "&flow=xtls-rprx-vision"
#         f"&security={env_config.settings.SECURITY}"
#         f"&sni={env_config.settings.HOST}"
#         f"&fp={env_config.settings.FINGERPRINT}"
#         f"&pbk={env_config.settings.PUBLICKEY}"
#         f"&sid={env_config.settings.SHORTID}"
#         f"&type={env_config.settings.NET_TYPE}#{email}"
#     )
#     return vless_link
