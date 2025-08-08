import database.models

import faststream.rabbit
import logic.payment_system


def can_user_buy_product(
    product: database.models.Product,
    finance_account: database.models.FinanceAccount,
) -> bool:
    return finance_account.balance >= product.price


async def make_a_purchase(
    message_id: int,
    user: database.models.TelegramUser,
    product: database.models.Product,
    finance_account: database.models.FinanceAccount,
    broker: faststream.rabbit.RabbitBroker,
):
    if not can_user_buy_product(product, finance_account):
        await broker.publish(
            {
                "user_id": user.telegram_id,
                "message_id": message_id,
            },
            queue="insufficient_funds",
        )
        return
    payment: database.models.Payment = (
        await logic.payment_system.create_withdrawal_payment(
            finance_account,
            product,
        )
    )
    # create product
    ...
    # end create product
    finance_account = await logic.payment_system.execute_withdrawal_payment(
        payment,
        finance_account,
    )
    await broker.publish(
        {
            "user_id": user.telegram_id,
            "message_id": message_id,
            "another": ...,
        },
        queue="create_purchase",
    )
