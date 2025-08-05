import database.core
import database.models
import sqlalchemy
import sqlalchemy.orm


async def is_moderator(
    user_id: int,
) -> bool:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(database.models.Moderator).where(
            database.models.Moderator.user_id == user_id
        )
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()
        return obj is not None


async def get_moderator_telegram_id_list() -> list[int]:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(
            database.models.TelegramUser.telegram_id
        ).join(
            database.models.Moderator,
            database.models.Moderator.user_id
            == database.models.TelegramUser.id,
        )
        result = await session.execute(stmt)
        telegram_ids = result.scalars().all()
        return telegram_ids
