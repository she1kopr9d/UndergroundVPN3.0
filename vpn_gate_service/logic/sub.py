import database.models
import database.io.base
import database.io.sub


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
