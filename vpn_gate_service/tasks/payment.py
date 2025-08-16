import celery_app

import database.io
import database.io.base
import database.models

import logic.payment_system

import rabbit


@celery_app.app.async_task_with_broker(name="tasks.withdrawal_payment")
async def withdrawal_payment(
    data: dict,
) -> int | None:
    user_id: int = data["user_id"]
    product_id: int = data["product_id"]
    user: database.models.TelegramUser = (
        await database.io.base.get_object_by_field(
            field=database.models.TelegramUser.telegram_id,
            value=user_id,
            object_class=database.models.TelegramUser,
        )
    )
    finance_account: database.models.FinanceAccount = (
        await database.io.base.get_object_by_field(
            field=database.models.FinanceAccount.user_id,
            value=user.id,
            object_class=database.models.FinanceAccount,
        )
    )
    product: database.models.Product = await database.io.base.get_object_by_id(
        id=product_id,
        object_class=database.models.Product,
    )
    payment: database.models.Payment = (
        await logic.payment_system.create_withdrawal_payment(
            finance_account=finance_account,
            product=product,
        )
    )
    if finance_account.balance >= payment.amount:
        finance_account: database.models.FinanceAccount = (
            await logic.payment_system.execute_withdrawal_payment(
                payment=payment,
                finance_account=finance_account,
            )
        )
        await rabbit.broker.publish(
            {
                "user_id": data.user_id,
                "amount": payment.amount,
                "now_balance": finance_account.balance,
                "status": "first",
            },
            queue="execute_withdrawal_payment",
        )
        return payment.id
    else:
        await rabbit.broker.publish(
            {
                "user_id": data.user_id,
                "amount": payment.amount,
                "now_balance": finance_account.balance,
                "status": "error",
            },
            queue="error_withdrawal_payment",
        )
        return payment.id
