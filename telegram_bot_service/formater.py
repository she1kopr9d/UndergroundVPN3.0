import datetime


def format_server_info(data: dict) -> str:
    if data.get("status") != "ok":
        return "Ошибка получения данных."

    text_lines = []
    for server_key, server_list in data["data"].items():
        server_info = server_list[0]
        timestamp = server_list[1]

        dt = datetime.datetime.fromtimestamp(timestamp)
        dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        text_lines.append(f"📡 Сервер: *{server_info.get('name')}*")
        text_lines.append(f"  IP: `{server_info.get('ip')}`")
        text_lines.append(f"  Порт: {server_info.get('port')}")
        text_lines.append(f"  API версия: {server_info.get('api_version')}")
        text_lines.append(f"  Обновлено: {dt_str}")
        text_lines.append("")

    return "\n".join(text_lines)
