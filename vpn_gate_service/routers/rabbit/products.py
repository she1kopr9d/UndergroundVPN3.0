import config
import database.io.base
import database.models
import faststream.rabbit.fastapi
import logic.buy_product
import schemas.product
import products_exec
import products_exec.abs.base

router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("buy_product")
async def buy_product_handler(
    data: schemas.product.BuyProductData,
):
    user: database.models.TelegramUser = (
        await database.io.base.get_object_by_field(
            field=database.models.TelegramUser.telegram_id,
            value=data.user_id,
            object_class=database.models.TelegramUser,
        )
    )
    finance_account: database.models.FinanceAccount = (
        await database.io.base.get_object_by_field(
            field=database.models.FinanceAccount.user_id,
            value=user.id,
            object_class=database.models.FinanceAccount,
        )
    )
    product: database.models.Product = await database.io.base.get_object_by_id(
        id=data.product_id,
        object_class=database.models.Product,
    )
    product_exec_obj: products_exec.abs.base.Product = (
        products_exec.get_exec_from_product_id(
            product_id=product.id,
        )
    )
    is_ready: bool = await product_exec_obj.сheck(user.telegram_id)
    if not is_ready:
        raise Exception("Not ready to buy this product")
    else:
        await logic.buy_product.make_a_purchase(
            user=user,
            product=product,
            finance_account=finance_account,
            broker=router.broker,
        )
