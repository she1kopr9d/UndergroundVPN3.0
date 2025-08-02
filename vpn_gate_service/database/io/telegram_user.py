import sqlalchemy
import sqlalchemy.orm

import database.core
import database.models

import schemas.dev
import schemas.telegram


async def create_telegram_user(
    data: schemas.telegram.StartData,
    referrer_id: int | None = None,
) -> database.models.TelegramUser:
    async with database.core.async_session_factory() as session:
        new_user = database.models.TelegramUser(
            telegram_id=data.user_id,
            username=data.username,
            referrer_id=referrer_id,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def telegram_user_exist(data: schemas.telegram.StartData):
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(database.models.TelegramUser).where(
            database.models.TelegramUser.telegram_id == data.user_id,
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user is not None


async def set_admin(data: schemas.dev.AddAdmin):
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.update(database.models.TelegramUser)
            .where(database.models.TelegramUser.telegram_id == data.user_id)
            .values(is_admin=True)
        )
        await session.execute(stmt)
        await session.commit()


async def user_is_admin(data: schemas.telegram.UserData) -> bool:
    async with database.core.async_session_factory() as session:
        result = await session.execute(
            sqlalchemy.select(database.models.TelegramUser.is_admin).where(
                database.models.TelegramUser.telegram_id == data.user_id
            )
        )
        is_admin = result.scalar_one_or_none()
        return bool(is_admin)


async def get_telegram_user_data(
    user_id: int,
) -> schemas.telegram.UserAllData | None:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(database.models.TelegramUser).where(
            database.models.TelegramUser.telegram_id == user_id
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return schemas.telegram.UserAllData(
            id=user.id,
            user_id=user.telegram_id,
            username=user.username,
            is_admin=user.is_admin,
        )


async def get_referrer_username(
    telegram_id: int,
) -> str | None:
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.select(database.models.TelegramUser)
            .options(
                sqlalchemy.orm.selectinload(
                    database.models.TelegramUser.referrer,
                )
            )
            .where(database.models.TelegramUser.telegram_id == telegram_id)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user and user.referrer:
            return user.referrer.username
        return None
