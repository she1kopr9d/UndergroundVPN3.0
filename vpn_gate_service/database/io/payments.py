import database.core
import database.models
import schemas.telegram
import sqlalchemy


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
) -> None:
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.update(database.models.Payment)
            .where(database.models.Payment.id == payment_id)
            .values(status=new_status)
            .returning(database.models.Payment)
        )
        result = await session.execute(stmt)
        await session.commit()


async def get_moderation_payments_with_pagination(
    data: schemas.telegram.PayPage,
) -> tuple[list[schemas.telegram.PaymentMinInfo], int]:
    async with database.core.async_session_factory() as session:
        stmt_count = sqlalchemy.select(sqlalchemy.func.count()).where(
            database.models.Payment.status
            == database.models.PaymentStatus.moderation
        )
        count_result = await session.execute(stmt_count)
        total_count = count_result.scalar_one()

        max_page = max(
            (total_count + data.pagination - 1) // data.pagination,
            1,
        )
        stmt_payments = (
            sqlalchemy.select(database.models.Payment)
            .where(
                database.models.Payment.status
                == database.models.PaymentStatus.moderation
            )
            .offset(data.page * data.pagination)
            .limit(data.pagination)
            .order_by(database.models.Payment.created_at.desc())
        )
        result = await session.execute(stmt_payments)
        payments = result.scalars().all()
        return [
            schemas.telegram.PaymentMinInfo(
                payment_id=payment.id,
                payment_method=payment.payment_method.value,
            )
            for payment in payments
        ], max_page


async def set_external_id(
    payment_id: int,
    external_id: str,
):
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.update(database.models.Payment)
            .where(database.models.Payment.id == payment_id)
            .values(external_id=external_id)
        )

        await session.execute(stmt)
        await session.commit()
