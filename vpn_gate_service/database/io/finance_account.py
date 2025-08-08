import database.core
import database.models
import sqlalchemy
import sqlalchemy.orm


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


async def add_amount_on_balance(
    finance_account_id: int,
    amount: float,
) -> database.models.FinanceAccount:
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.update(database.models.FinanceAccount)
            .where(database.models.FinanceAccount.id == finance_account_id)
            .values(balance=database.models.FinanceAccount.balance + amount)
            .returning(database.models.FinanceAccount)
        )
        result = await session.execute(stmt)
        finance_account = result.scalar_one()
        await session.commit()
        await session.refresh(finance_account)
        return finance_account


async def withdrawal_on_balance(
    finance_account_id: int,
    amount: float,
) -> database.models.FinanceAccount:
    return (await add_amount_on_balance(
        finance_account_id=finance_account_id,
        amount=-amount,
    ))
