import config
import os
import database.io.base
import database.io.finance_account
import database.io.payments
import database.io.telegram_user
import database.io.receipt
import database.models
import faststream.rabbit.fastapi
import logic.payment_system
import schemas.deposit
import schemas.telegram

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


@router.subscriber("accept_deposit")
async def accept_deposit_handle(
    data: schemas.deposit.DepositeMoveData,
):
    await database.io.payments.update_payment_status(
        data.payment_id,
        database.models.PaymentStatus.moderation,
    )
    await router.broker.publish(
        queue="new_moderation_payment",
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
            "payment_id": data.payment_id,
        },
        queue="accept_deposit_answer",
    )


@router.subscriber("cancel_deposit")
async def cansel_deposit_handle(
    data: schemas.deposit.DepositeMoveData,
):
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
