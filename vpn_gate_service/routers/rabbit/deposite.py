import faststream.rabbit.fastapi

import config

import database.models
import database.io.telegram_user
import database.io.payments
import database.io.finance_account
import database.io.base

import schemas.deposit
import schemas.telegram

import logic.payment_system


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("create_payment")
async def create_payment_handle(
    data: schemas.deposit.DepositeCreate,
):
    is_handle = await database.io.telegram_user.user_is_handle(
        schemas.telegram.UserData(user_id=data.user_id),
    )
    if not is_handle:
        if data.method == database.models.PaymentMethod.handle:
            return
    user_all_data = await database.io.telegram_user.get_telegram_user_data(
        user_id=data.user_id,
    )
    finance_account_obj = (
        await database.io.finance_account.get_finance_account(
            user_id=user_all_data.id,
        )
    )
    payment_obj = await database.io.payments.create_payment(
        account_id=finance_account_obj.id,
        amount=float(data.amount),
        transaction_type=database.models.TransactionType.deposit,
        payment_method=data.method,
        mode=(
            database.models.PaymentMode.production
            if data.method != database.models.PaymentMethod.system
            else database.models.PaymentMode.test
        ),
    )
    requisite, currency = logic.payment_system.get_requisite(
        data.method,
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
            "payment_id": payment_obj.id,
            "requisite": requisite,
            "currency": currency,
            "amount": logic.payment_system.get_amount(
                data.amount,
                data.method,
            ),
            "method": data.method,
        },
        queue="create_payment_answer",
    )
