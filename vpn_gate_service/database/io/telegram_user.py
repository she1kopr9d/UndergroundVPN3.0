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
