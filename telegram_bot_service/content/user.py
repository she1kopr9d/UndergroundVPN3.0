import schemas.user


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

Также вам начислен бонус в размере 100 рублей на баланс
Его хватит для покупки пробного конфига на 7 дней
"""


def HELP_COMMAND() -> str:
    return """
<b>Список всех команд</b>

<b>Общее</b>
/start - запуск пользования ботом
/help - отображение команд с пояснением
/app - скидывает ссылки для установки

<b>Профиль</b>
/profile - выводит ваш профиль с данными
/balance - выводит информацию платежного аккаунта
/ref - выводит вашу реферальную ссылку и статистику

<b>Конфиги</b>
/conf - выводит вам все ваши конфиги

<b>Платежи</b>
/payment - выводит меню для пополнения баланса
"""


def APP_COMMAND() -> str:
    return """
<b>Ссылки на приложения под разные платформы</b>

<a href="https://play.google.com/store/apps/details?id=com.v2raytun.android">Андройд</a>

<a href="https://apps.apple.com/en/app/v2raytun/id6476628951">IOS</a>

<a href="https://v2raytun-install.ru/v2RayTun_Setup.exe">Windows</a>

<a href="https://apps.apple.com/en/app/v2raytun/id6476628951">MacOS</a>
"""


def GUIDE_COMMAND() -> str:
    return """
<a href="https://telegra.ph/Gajd-po-ispolzovaniyu-V2RayTun-08-22-2">Ссылка на гайд</a>

"""


def PROFILE_COMMAND(
    profile_data: schemas.user.ProfileData,
    bot_username: str,
) -> str:
    return f"""
<b>Профиль пользователя</b>

<b>Id:</b> {profile_data.user_id}
<b>Никнейм:</b> {profile_data.username}
<b>Баланс:</b> {profile_data.balance}
<b>Процент с рефералов:</b> {profile_data.referral_percentege}%


🔗 <b>Ваша реферальная ссылка</b>:
<code>https://t.me/{bot_username}?start={profile_data.user_id}</code>
"""


def REF_COMMAND(
    referral_percentage: int,
    referrer_username: str,
) -> str:
    referrer_username = (
        referrer_username if referrer_username is not None else "Отсутствует"
    )
    return f"""
<b>Информация о рефералах</b>

<b>Вы реферал у</b> @{referrer_username}

<b>Ваш процент с рефералов:</b> {referral_percentage}%
"""


def REFERRAL_DEPOSIT(
    data: schemas.user.ReferralDepositInfo,
) -> str:
    return f"""
Реферал @{data.referral_username} пополнил баланс

Вам на счет добавленно {data.amount} рублей
"""
