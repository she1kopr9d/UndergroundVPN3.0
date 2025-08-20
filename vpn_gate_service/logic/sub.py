import database.models
import database.io.base
import database.io.sub
import logic.payment_system
import rabbit
import products_exec


async def create_sub(
    user_id: int,
    product_id: int,
    payment: database.models.Payment,
):
    product: database.models.Product = await database.io.base.get_object_by_id(
        id=product_id,
        object_class=database.models.Product,
    )
    subscription: database.models.Subscription = (
        await database.io.sub.create_subscription_with_duration(
            user_id=user_id,
            product_id=product_id,
            days=product.duration_days,
            payment_id=payment.id,
        )
    )
    return subscription


async def update_sub(
    subscription_id: int,
):
    subscription: database.models.Subscription = (
        await database.io.base.get_object_by_id(
            id=subscription_id,
            object_class=database.models.Subscription,
        )
    )
    user: database.models.TelegramUser = (
        await database.io.base.get_object_by_id(
            id=subscription.user_id,
            object_class=database.models.TelegramUser,
        )
    )
    payment: database.models.Payment = (
        await logic.payment_system.withdrawal_payment(
            user_id=user.telegram_id,
            product_id=subscription.product_id,
            broker=rabbit.broker,
        )
    )
    product: database.models.Product = await database.io.base.get_object_by_id(
        id=subscription.product_id,
        object_class=database.models.Product,
    )
    match payment.status.value:
        case database.models.PaymentStatus.failed.value:
            await rabbit.broker.publish(
                {
                    "user_id": user.telegram_id,
                    "text": (
                        "Подписка была отключена, тк у вас "
                        "недостаточно средств для продления"
                    ),
                    "photo": None,
                },
                queue="send_telegram_message",
            )
            exec_product: database.models.ExecuteProduct = (
                await database.io.base.get_object_by_field(
                    field=database.models.ExecuteProduct.product_id,
                    value=product.id,
                    object_class=database.models.ExecuteProduct,
                )
            )
            exec_obj = products_exec.exec_list[exec_product.executor_name]()
            await exec_obj.remove(user.telegram_id, subscription.id)
            await database.io.sub.set_subscription_inactive(
                subscription_id=subscription_id,
            )
        case database.models.PaymentStatus.completed.value:
            await database.io.sub.extend_subscription(
                subscription_id=subscription_id,
                days=product.duration_days,
                payment_id=payment.id,
            )
            await rabbit.broker.publish(
                {
                    "user_id": user.telegram_id,
                    "text": "Подписка продленна",
                    "photo": None,
                },
                queue="send_telegram_message",
            )
