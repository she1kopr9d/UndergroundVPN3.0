import sqlalchemy

import database.core
import database.models


async def create_payment(
    account_id: int,
    amount: float,
    transaction_type: database.models.TransactionType,
    payment_method: database.models.PaymentMethod,
    note: str | None = None,
    external_id: str | None = None,
    mode: database.models.PaymentMode = database.models.PaymentMode.production,
) -> database.models.Payment:
    async with database.core.async_session_factory() as session:
        new_payment = database.models.Payment(
            amount=amount,
            transaction_type=transaction_type,
            payment_method=payment_method,
            status=database.models.PaymentStatus.pending,
            finance_account_id=account_id,
            note=note,
            external_id=external_id,
            mode=mode,
        )
        session.add(new_payment)
        await session.commit()
        await session.refresh(new_payment)
        return new_payment


async def update_payment_status(
    payment_id: int,
    new_status: database.models.PaymentStatus,
) -> bool:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.update(database.models.Payment).where(
            database.models.Payment.id == payment_id
        ).values(status=new_status)

        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0
