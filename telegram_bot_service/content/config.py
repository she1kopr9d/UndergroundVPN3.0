import datetime

import schemas.config

MONTHS = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


def format_date(date: datetime.datetime | None) -> str:
    if date is None:
        return "безлимитная"
    return f"{date.day} {MONTHS[date.month]} {date.year} года"


def CONFIG_INFO(
    data: schemas.config.ConfigInfoANSW,
) -> str:
    return f"""
Информация конфига:

*Сервер*: {data.server_name}
*Название конфига*: {data.config_name}

*Дата окончания*: {format_date(data.end_date)}


*Ссылка на конфиг*
`{data.config_url}`
"""


def CONFIG_DELETE_QUESTION() -> str:
    return """
Вы уверены, что хотите удалить конфиг?
Это безвозвратно его очистит с сервера

!!! за него не вернутся денюжные стредства
"""


def CONFIG_CANCEL_QUESTION() -> str:
    return """
Вы уверены, что хотите отменить подписку?
В случае отмены, конфиг будет действовать
до конца подписки, а после не продлится
"""
