import sqlalchemy

import database.database
import database.models
import schemas.telegram


async def create_telegram_user(data: schemas.telegram.StartData):
    async with database.database.async_session_factory() as session:
        new_user = database.models.TelegramUser(
            telegram_id=data.user_id,
            username=data.username,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)


async def telegram_user_exist(data: schemas.telegram.StartData):
    async with database.database.async_session_factory() as session:
        stmt = sqlalchemy.select(database.models.TelegramUser).where(
            database.models.TelegramUser.telegram_id == data.user_id,
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user is not None
