import os

import config
import database.io.base
import database.io.finance_account
import database.io.payments
import database.io.receipt
import database.io.telegram_user
import database.models
import faststream.rabbit.fastapi
import logic.payment_system
import schemas.deposit
import schemas.telegram
import logic.crypto_dep


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

    requisite, currency, amount = await logic.payment_system.create_payment(
        payment=payment_obj,
    )

    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
            "payment_id": payment_obj.id,
            "requisite": requisite,
            "currency": currency,
            "amount": amount,
            "method": data.method,
        },
        queue="create_payment_answer",
    )


@router.subscriber("accept_deposit")
async def accept_deposit_handle(
    data: schemas.deposit.DepositeMoveData,
):
    payment_obj: database.models.Payment = (
        await database.io.base.get_object_by_id(
            id=data.payment_id,
            object_class=database.models.Payment,
        )
    )
    await logic.payment_system.accept_payment(
        payment_obj,
        router.broker,
        data.user_id,
        data.message_id,
    )


@router.subscriber("cancel_deposit")
async def cansel_deposit_handle(
    data: schemas.deposit.DepositeMoveData,
):
    payment: database.models.Payment = await database.io.base.get_object_by_id(
        id=data.payment_id,
        object_class=database.models.Payment,
    )
    if (
        payment.payment_method.value
        == database.models.PaymentMethod.crypto.value
    ):
        if await logic.crypto_dep.check_paid_payment_status(payment):
            await logic.crypto_dep.valid_accept_payment(
                payment,
                router.broker,
                data.user_id,
                data.message_id,
            )
    await database.io.payments.update_payment_status(
        data.payment_id,
        database.models.PaymentStatus.failed,
    )


@router.subscriber("save_payment_receipt")
async def save_payment_receipt(
    data: schemas.deposit.DepositReceiptUploadData,
):
    file_bytes = data.filebytes.encode("latin1")
    folder_path = f"uploads/receipts/{data.payment_id}"
    os.makedirs(folder_path, exist_ok=True)
    full_path = os.path.join(folder_path, data.filename)

    with open(full_path, "wb") as f:
        f.write(file_bytes)
    await database.io.receipt.add_payment_receipt(
        data.payment_id,
        data.filename,
        full_path,
    )


@router.subscriber("accept_deposit_moder")
async def accept_deposit_moder_handler(
    data: schemas.deposit.DepositeMoveData,
):
    payment_obj: database.models.Payment = (
        await database.io.base.get_object_by_id(
            id=data.payment_id,
            object_class=database.models.Payment,
        )
    )
    finance_account_obj: database.models.FinanceAccount = (
        await database.io.finance_account.add_amount_on_balance(
            finance_account_id=payment_obj.finance_account_id,
            amount=payment_obj.amount,
        )
    )
    user_obj: database.models.TelegramUser = (
        await database.io.base.get_object_by_id(
            id=finance_account_obj.user_id,
            object_class=database.models.TelegramUser,
        )
    )
    await database.io.payments.update_payment_status(
        payment_id=data.payment_id,
        new_status=database.models.PaymentStatus.completed,
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
        },
        queue="accept_deposit_moder_answer",
    )
    await router.broker.publish(
        {
            "user_id": user_obj.telegram_id,
            "message_id": data.message_id,
        },
        queue="accept_deposit_moder_to_client",
    )
    await logic.payment_system.accept_payment_referrer_notification(
        user_obj,
        payment_obj,
        router.broker,
    )


@router.subscriber("cancel_deposit_moder")
async def cancel_deposit_moder_handler(
    data: schemas.deposit.DepositeMoveData,
):
    await database.io.payments.update_payment_status(
        payment_id=data.payment_id,
        new_status=database.models.PaymentStatus.failed,
    )
    payment_obj: database.models.Payment = (
        await database.io.base.get_object_by_id(
            id=data.payment_id,
            object_class=database.models.Payment,
        )
    )
    finance_account_obj: database.models.FinanceAccount = (
        await database.io.base.get_object_by_id(
            id=payment_obj.finance_account_id,
            object_class=database.models.FinanceAccount,
        )
    )
    user_obj: database.models.TelegramUser = (
        await database.io.base.get_object_by_id(
            id=finance_account_obj.user_id,
            object_class=database.models.TelegramUser,
        )
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
        },
        queue="cancel_deposit_moder_answer",
    )
    await router.broker.publish(
        {
            "user_id": user_obj.telegram_id,
        },
        queue="cancel_deposit_moder_to_client",
    )
