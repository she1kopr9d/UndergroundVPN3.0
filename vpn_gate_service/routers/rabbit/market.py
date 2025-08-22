import config
import database.io.base
import database.io.finance_account
import database.io.payments
import database.io.receipt
import database.io.telegram_user
import database.models
import faststream.rabbit.fastapi
import logic.payment_system
import logic.sub
import products_exec
import products_exec.abs.base
import schemas.deposit
import schemas.product
import schemas.telegram

router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("product_info")
async def product_info_handle(
    data: schemas.product.ProductGetPaggination,
):
    product: database.models.Product = await database.io.base.get_object_by_id(
        id=data.product_id,
        object_class=database.models.Product,
    )
    product_schema = schemas.product.ProductView(
        user_id=data.user_id,
        message_id=data.message_id,
        product_id=product.id,
        page=data.page,
        product_name=product.name,
        product_price=product.price,
        product_type=product.product_type,
        duration_days=product.duration_days,
    )
    await router.broker.publish(
        product_schema.dict(),
        queue="product_info_answer",
    )


@router.subscriber("product_buy")
async def product_buy_handle(
    data: schemas.product.ProductGet,
):
    payment: database.models.Payment = (
        await logic.payment_system.withdrawal_payment(
            user_id=data.user_id,
            product_id=data.product_id,
            status="first",
            broker=router.broker,
        )
    )
    if payment.status.value == database.models.PaymentStatus.failed.value:
        return
    user: database.models.TelegramUser = (
        await database.io.base.get_object_by_field(
            field=database.models.TelegramUser.telegram_id,
            value=data.user_id,
            object_class=database.models.TelegramUser,
        )
    )
    subscription: database.models.Subscription = await logic.sub.create_sub(
        user_id=user.id,
        product_id=data.product_id,
        payment=payment,
    )
    exec_product: database.models.ExecuteProduct = (
        await database.io.base.get_object_by_field(
            field=database.models.ExecuteProduct.product_id,
            value=data.product_id,
            object_class=database.models.ExecuteProduct,
        )
    )

    exec_obj: products_exec.abs.base.Product = products_exec.exec_list[
        exec_product.executor_name
    ]()
    await exec_obj.create(
        user_id=data.user_id,
        subscription_id=subscription.id,
    )
