import docker
import json
import pathlib
import shutil
import typing

import app.config


def load_config() -> dict[str, typing.Any]:
    with open(app.config.settings.config_path, "r") as f:
        return json.load(f)


def restart_xray_container():
    try:
        client = docker.DockerClient(base_url="unix://var/run/docker.sock")
        container = client.containers.get("xray")
        container.restart()
        print("Xray container restarted successfully.")
    except docker.errors.NotFound:
        print("Xray container not found.")
    except docker.errors.APIError as e:
        print(f"Error restarting Xray container: {e}")


def save_config(config: dict[str, typing.Any]) -> None:
    path: pathlib.Path = app.config.settings.config_path
    backup_path: pathlib.Path = path.with_suffix(".bak")
    shutil.copy2(path, backup_path)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    restart_xray_container()


def find_inbound(config: dict[str, typing.Any]) -> dict[str, typing.Any]:
    for inbound in config.get("inbounds", []):
        return inbound
    raise ValueError(
        f"Inbound с тегом '{app.config.settings.inbound_tag}' не найден"
    )


def add_user_to_config(
    config: dict[str, typing.Any], email: str, uuid: str
) -> None:
    inbound = find_inbound(config)
    settings = inbound.setdefault("settings", {})
    clients = settings.setdefault("clients", [])

    # Проверка на дубликаты
    for client in clients:
        if client.get("email") == email or client.get("id") == uuid:
            raise ValueError("Пользователь уже существует")

    # Добавление клиента
    clients.append({
        "id": uuid,
        "email": email,
        "level": 0,
        "flow": "xtls-rprx-vision"
    })


def remove_user_from_config(
    config: dict[str, typing.Any], email: str, uuid: str
) -> None:
    inbound = find_inbound(config)
    settings = inbound.get("settings", {})
    clients = settings.get("clients", [])

    updated_clients = [
        client for client in clients
        if not (client.get("email") == email and client.get("id") == uuid)
    ]

    if len(updated_clients) == len(clients):
        raise ValueError("Пользователь не найден в конфиге")

    # Применяем обновлённый список
    settings["clients"] = updated_clients


def generate_url(email: str, uuid: str) -> str:
    vless_link = (
        "vless://"
        f"{uuid}@{app.config.settings.DOMAIN}:{app.config.settings.VPN_PORT}"
        f"?encryption={app.config.settings.ENCRYPTION}"
        "&flow=xtls-rprx-vision"
        f"&security={app.config.settings.SECURITY}"
        f"&sni={app.config.settings.HOST}"
        f"&fp={app.config.settings.FINGERPRINT}"
        f"&pbk={app.config.settings.PUBLICKEY}"
        f"&sid={app.config.settings.SHORTID}"
        f"&type={app.config.settings.NET_TYPE}#{email}"
    )
    return vless_link
