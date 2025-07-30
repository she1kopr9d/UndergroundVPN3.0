def START_COMMAND(
    server_count: int = 1,
    country_count: int = 1,
    vpn_technologie: str = "XRay + Reality",
    referral_rercentage: int = 15,
    profile_command: str = "profile",
    bot_username: str = "undeground_vpn",
    ref_code: str = "12345678",
) -> str:
    return f"""
Приветствую. Я бот по продаже VPN.

У нас {server_count} серверов в {country_count} странах.
Мы используем технологию {vpn_technologie}.

У нас также есть система рефералов:
С каждой покупки реферала вы будете получать по {referral_rercentage}%.
(Процент может поменяться со временем, в /{profile_command} можно его увидеть)

🔗 *Ваша реферальная ссылка*:
`https://t.me/{bot_username}?start={ref_code}`
"""


def VIEW_CONFIG(
    config: str,
) -> str:
    return f"""
Ваш конфиг сгенерирован:

`{config}`
"""


def NEW_REFERRAL(
    referrer_username: str,
) -> str:
    return f"""
Поздравляем, у вас новый реферал

@{referrer_username}
"""


def REFERRAL_TEXT(
    referrer_username: str,
) -> str:
    return f"""

Вас позвал в наш коллектив @{referrer_username}
"""
