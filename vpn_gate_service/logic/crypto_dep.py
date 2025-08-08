import aiocryptopay
import aiocryptopay.models.invoice
import config
import database.io.base
import database.io.finance_account
import database.io.payments
import database.models
import faststream.rabbit
import utils.binance.currency_exchage_rate

crypto = aiocryptopay.AioCryptoPay(
    token=config.crypto.get_token,
    network=config.crypto.get_net,
)


async def new_invoice(amount: float) -> aiocryptopay.models.invoice.Invoice:
    invoice: aiocryptopay.models.invoice.Invoice = await crypto.create_invoice(
        asset="USDT", amount=amount
    )
    return invoice


async def get_invoice(
    external_id: str,
) -> aiocryptopay.models.invoice.Invoice:
    returned = await crypto.get_invoices(invoice_ids=int(external_id))
    return returned


async def create_crypto_payment(
    payment: database.models.Payment,
) -> str:
    amount_usdt = (
        await utils.binance.currency_exchage_rate.get_rub_to_usdt_binance()
    ) * payment.amount
    invoice: aiocryptopay.models.invoice.Invoice = await new_invoice(
        amount=amount_usdt
    )
    await database.io.payments.set_external_id(
        payment_id=payment.id,
        external_id=str(invoice.invoice_id),
    )
    return invoice.bot_invoice_url, amount_usdt


async def check_paid_payment_status(
    payment: database.models.Payment,
) -> bool:
    invoice: aiocryptopay.models.invoice.Invoice = await get_invoice(
        payment.external_id
    )
    return invoice.status == "paid"


async def accept_payment(
    payment: database.models.Payment,
    broker: faststream.rabbit.RabbitBroker,
    user_id: int,
    message_id: int,
):
    if await check_paid_payment_status(payment):
        await database.io.finance_account.add_amount_on_balance(
            finance_account_id=payment.finance_account_id,
            amount=payment.amount,
        )
        await database.io.payments.update_payment_status(
            payment_id=payment.id,
            new_status=database.models.PaymentStatus.completed,
        )
        await broker.publish(
            {
                "user_id": user_id,
                "message_id": message_id,
            },
            queue="accept_deposit_moder_to_client",
        )
    else:
        await broker.publish(
            {
                "user_id": user_id,
                "message_id": message_id,
            },
            "crypto_payment_not_paid",
        )
