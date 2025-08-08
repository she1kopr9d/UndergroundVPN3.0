import config
import database.io.base
import database.io.finance_account
import database.io.payments
import database.models
import faststream.rabbit.fastapi
import logic.crypto_dep


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
            await logic.crypto_dep.accept_payment(
                payment, broker, user_id, message_id
            )
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
        case database.models.PaymentMethod.telegram_star.value:
            pass
