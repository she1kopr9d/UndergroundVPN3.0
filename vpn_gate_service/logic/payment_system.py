import config
import database.io.base
import database.io.finance_account
import database.io.payments
import database.models
import faststream.rabbit.fastapi
import logic.crypto_dep
import logic.payment_system


async def create_payment(
    payment: database.models.Payment,
):
    match payment.payment_method.value:
        case database.models.PaymentMethod.crypto.value:
            link, amount = await logic.crypto_dep.create_crypto_payment(
                payment
            )
            return (link, "USDT", amount)
        case database.models.PaymentMethod.handle.value:
            return (
                config.payment.HANDLE_ADDRESS,
                config.payment.HANDLE_CURRENCY,
                payment.amount,
            )
        case database.models.PaymentMethod.telegram_star.value:
            return (None, "STAR", payment.amount * 2.5)
        case database.models.PaymentMethod.system.value:
            return ("Тестовые реквизиты для тестов", "BTC", 0.0)


async def accept_handle_payment_to_moderator(
    payment: database.models.Payment,
    broker: faststream.rabbit.RabbitBroker,
    user_id: int,
    message_id: int,
):
    await database.io.payments.update_payment_status(
        payment.id,
        database.models.PaymentStatus.moderation,
    )
    await broker.publish(
        queue="new_moderation_payment",
    )
    await broker.publish(
        {
            "user_id": user_id,
            "message_id": message_id,
            "payment_id": payment.id,
        },
        queue="accept_deposit_answer",
    )


async def accept_payment_referrer_notification(
    user_obj: database.models.TelegramUser,
    payment_obj: database.models.Payment,
    broker: faststream.rabbit.RabbitBroker,
):
    if user_obj.referrer_id is not None:
        referrer_user_obj: database.models.TelegramUser = (
            await database.io.base.get_object_by_id(
                id=user_obj.referrer_id,
                object_class=database.models.TelegramUser,
            )
        )
        referrer_finance_account_obj: database.models.FinanceAccount = (
            await database.io.finance_account.get_finance_account(
                user_id=referrer_user_obj.id,
            )
        )
        referral_percent = referrer_finance_account_obj.referral_percent
        referral_amount = payment_obj.amount * referral_percent / 100
        await database.io.finance_account.add_amount_on_balance(
            finance_account_id=referrer_finance_account_obj.id,
            amount=referral_amount,
        )
        await broker.publish(
            {
                "referral_user_id": user_obj.telegram_id,
                "referral_username": user_obj.username,
                "user_id": referrer_user_obj.telegram_id,
                "amount": referral_amount,
            },
            queue="now_referral_deposit",
        )


async def crypto_accept_payment(
    payment: database.models.Payment,
    broker: faststream.rabbit.RabbitBroker,
    user_id: int,
    message_id: int,
):
    is_ok = await logic.crypto_dep.accept_payment(
        payment, broker, user_id, message_id
    )
    if is_ok:
        user_obj: database.models.TelegramUser = (
            await database.io.base.get_object_by_field(
                field=database.models.TelegramUser.telegram_id,
                value=user_id,
                object_class=database.models.TelegramUser,
            )
        )
        await accept_payment_referrer_notification(
            user_obj,
            payment,
            broker,
        )


async def accept_payment(
    payment: database.models.Payment,
    broker: faststream.rabbit.RabbitBroker,
    user_id: int,
    message_id: int,
):
    match payment.payment_method.value:
        case database.models.PaymentMethod.handle.value:
            await accept_handle_payment_to_moderator(
                payment, broker, user_id, message_id
            )
        case database.models.PaymentMethod.system.value:
            await accept_handle_payment_to_moderator(
                payment, broker, user_id, message_id
            )
        case database.models.PaymentMethod.crypto.value:
            await crypto_accept_payment(
                payment,
                broker,
                user_id,
                message_id,
            )
        case database.models.PaymentMethod.telegram_star.value:
            pass


async def create_withdrawal_payment(
    finance_account: database.models.FinanceAccount,
    product: database.models.Product,
) -> database.models.Payment:
    payment: database.models.Payment = (
        await database.io.payments.create_payment(
            account_id=finance_account.id,
            amount=product.price,
            transaction_type=database.models.TransactionType.withdrawal,
            payment_method=database.models.PaymentMethod.system,
            mode=database.models.PaymentMode.production,
        )
    )
    return payment


async def execute_withdrawal_payment(
    payment: database.models.Payment,
    finance_account: database.models.FinanceAccount,
) -> database.models.FinanceAccount:
    if payment.status.value != database.models.PaymentStatus.pending.value:
        await database.io.base.update_field(
            object_class=database.models.Payment,
            search_field=database.models.Payment.id,
            search_value=payment.id,
            update_list={
                "status": database.models.PaymentStatus.failed,
            },
        )
        raise Exception("Payment has not valid status for withdrawal")
    finance_account = await database.io.finance_account.withdrawal_on_balance(
        finance_account_id=finance_account.id,
        amount=payment.amount,
    )
    await database.io.base.update_field(
        object_class=database.models.Payment,
        search_field=database.models.Payment.id,
        search_value=payment.id,
        update_list={
            "status": database.models.PaymentStatus.completed,
        },
    )
    return finance_account


async def withdrawal_payment(
    user_id: int,
    product_id: int,
    broker: faststream.rabbit.RabbitBroker,
    status: str = "add",
) -> database.models.Payment:
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
        await broker.publish(
            {
                "user_id": user_id,
                "amount": payment.amount,
                "now_balance": finance_account.balance,
                "status": status,
            },
            queue="execute_withdrawal_payment",
        )
    else:
        await database.io.payments.update_payment_status(
            payment_id=payment.id,
            new_status=database.models.PaymentStatus.failed,
        )
        payment: database.models.Payment = (
            await database.io.base.get_object_by_id(
                id=payment.id,
                object_class=database.models.Payment,
            )
        )
        await broker.publish(
            {
                "user_id": user_id,
                "amount": payment.amount,
                "now_balance": finance_account.balance,
                "status": "error",
            },
            queue="error_withdrawal_payment",
        )
    payment: database.models.Payment = await database.io.base.get_object_by_id(
        id=payment.id,
        object_class=database.models.Payment,
    )
    return payment
