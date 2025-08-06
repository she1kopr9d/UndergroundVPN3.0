import config
import database.io.base
import database.io.moderator
import database.io.payments
import database.io.telegram_user
import database.models
import faststream.rabbit.fastapi
import logic.receipt_convert
import schemas.deposit
import schemas.telegram

router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("pay_list_command")
async def pay_list_handler(
    data: schemas.telegram.PayPage,
):
    payments, max_page = (
        await database.io.payments.get_moderation_payments_with_pagination(
            data,
        )
    )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "message_id": data.message_id,
            "max_page": max_page,
            "now_page": data.page,
            "payments": payments,
        },
        queue="pay_list_command_answer",
    )


@router.subscriber("new_moderation_payment")
async def new_moderation_payment_alert():
    moderators_ids = (
        await database.io.moderator.get_moderator_telegram_id_list()
    )
    for moderator_id in moderators_ids:
        await router.broker.publish(
            {
                "user_id": moderator_id,
            },
            queue="new_moderation_payment_alert",
        )


@router.subscriber("pay_cell_moder_data")
async def pay_cell_moder_data_handler(
    data: schemas.deposit.DepositCellData,
):
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
    payment_receipt_obj: database.models.PaymentReceipt = (
        await database.io.base.get_object_by_field(
            field=database.models.PaymentReceipt.payment_id,
            value=data.payment_id,
            object_class=database.models.PaymentReceipt,
        )
    )
    payment_receipt_dict = None
    if payment_receipt_obj:
        payment_receipt_dict = await logic.receipt_convert.convert_payment_receipt_to_receipt_data(
            receipt=payment_receipt_obj,
        )
    await router.broker.publish(
        {
            "user_id": data.user_id,
            "user": {
                "user_id": user_obj.telegram_id,
                "username": user_obj.username,
            },
            "message_id": data.message_id,
            "now_page": data.now_page,
            "payment": {
                "payment_id": payment_obj.id,
                "amount": payment_obj.amount,
                "payment_method": payment_obj.payment_method.value,
                "receipt": payment_receipt_dict,
            },
        },
        queue="pay_cell_moder_data_answer",
    )
