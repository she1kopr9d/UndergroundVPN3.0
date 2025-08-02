import sqlalchemy
import sqlalchemy.orm

import database.core
import database.models


async def create_finance_account(
    user_id: int,
) -> database.models.FinanceAccount:
    async with database.core.async_session_factory() as session:
        finance_account = database.models.FinanceAccount(
            user_id=user_id,
        )
        session.add(finance_account)
        await session.commit()
        await session.refresh(finance_account)


async def get_finance_account(
    user_id: int,
):
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(database.models.FinanceAccount).where(
            database.models.FinanceAccount.user_id == user_id
        )
        finance_account = await session.scalar(stmt)
        return finance_account


async def get_referral_percentage(telegram_id: int) -> int:
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.select(database.models.TelegramUser)
            .options(
                sqlalchemy.orm.selectinload(
                    database.models.TelegramUser.finance_account
                )
            )
            .where(database.models.TelegramUser.telegram_id == telegram_id)
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.finance_account:
            return 0

        return user.finance_account.referral_percent
