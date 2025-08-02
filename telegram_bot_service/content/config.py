import schemas.config


def CONFIG_INFO(
    data: schemas.config.ConfigInfoANSW,
) -> str:
    return f"""
Информация конфига:

*Сервер*: {data.server_name}
*Название конфига*: {data.config_name}


*Ссылка на конфиг*
`{data.config_url}`
"""
