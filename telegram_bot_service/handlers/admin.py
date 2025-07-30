import httpx

import aiogram
import aiogram.types
import aiogram.filters.command

import config
import filters.is_admin
import formater
import rabbit
import content.admin


router = aiogram.Router()
router.message.filter(filters.is_admin.IsAdminFilter())


@router.message(
    aiogram.filters.command.Command("servers"),
)
async def get_servers_handler(message: aiogram.types.Message):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"{config.settings.GATE_URL}/server/active",
            )
            response.raise_for_status()
            data = response.json()
            await message.answer(
                formater.format_server_info(data),
                parse_mode="Markdown",
            )
        except httpx.HTTPStatusError as exc:
            await message.answer(
                (
                    f"Ошибка HTTP: {exc.response.status_code}"
                    f" - {exc.response.text}"
                )
            )
        except httpx.RequestError as exc:
            await message.answer(f"Ошибка запроса: {exc}")


@router.message(
    aiogram.filters.Command("cc"),
)
async def create_config_handler(message: aiogram.types.Message):
    if len(message.text.split()) < 2:
        await message.answer(
            ("Эта команда требует один аргумент" "/сc <server_name:str>")
        )
        return
    server_name = message.text.split()[1]
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "server_name": server_name,
        },
        queue="create_config",
    )
    await message.answer(content.admin.CREATE_CONFIG_PROCESS(server_name))


@router.message(
    aiogram.filters.Command("sc"),
)
async def create_server_handler(message: aiogram.types.Message):
    if len(message.text.split()) < 3:
        await message.answer(
            (
                "Эта команда требует двух аргументов"
                "/sc <server_name:str> <secret_key:str>"
            )
        )
        return
    server_name = message.text.split()[1]
    code = message.text.split()[2]
    await rabbit.broker.publish(
        {
            "user_id": message.from_user.id,
            "name": server_name,
            "secret_key": code,
        },
        queue="create_server",
    )
