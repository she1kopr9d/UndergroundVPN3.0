import database.core
import database.models


async def add_payment_receipt(
    payment_id: int,
    filename: str,
    file_path: str,
) -> database.models.PaymentReceipt:
    async with database.core.async_session_factory() as session:
        receipt = database.models.PaymentReceipt(
            payment_id=payment_id,
            filename=filename,
            file_path=file_path,
        )
        session.add(receipt)
        await session.commit()
        await session.refresh(receipt)
        return receipt
