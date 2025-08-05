import database.core
import database.models
import schemas.telegram
import sqlalchemy


async def get_referrals_with_pagination(
    data: schemas.telegram.RefPage,
) -> tuple[list[schemas.telegram.Referral], int]:
    async with database.core.async_session_factory() as session:
        stmt_user = sqlalchemy.select(database.models.TelegramUser).where(
            database.models.TelegramUser.telegram_id == data.user_id
        )
        result = await session.execute(stmt_user)
        user = result.scalar_one_or_none()

        if not user:
            return [], 1
        stmt_count = sqlalchemy.select(sqlalchemy.func.count()).where(
            database.models.TelegramUser.referrer_id == user.id
        )
        count_result = await session.execute(stmt_count)
        total_count = count_result.scalar_one()

        max_page = max(
            (total_count + data.pagination - 1) // data.pagination, 1
        )
        stmt_refs = (
            sqlalchemy.select(database.models.TelegramUser)
            .where(database.models.TelegramUser.referrer_id == user.id)
            .offset(data.page * data.pagination)
            .limit(data.pagination)
            .order_by(database.models.TelegramUser.created_at.desc())
        )
        result_refs = await session.execute(stmt_refs)
        referrals = result_refs.scalars().all()

        return [
            schemas.telegram.Referral(
                user_id=ref.telegram_id,
                username=ref.username,
            )
            for ref in referrals
        ], max_page
