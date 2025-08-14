import config
import database.io.base
import database.models
import faststream.rabbit.fastapi
import logic.buy_product
import schemas.product

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
    product: database.models.Product = (
        await database.io.base.get_object_by_id(
            id=data.product_id,
            object_class=database.models.Product,
        )
    )
    await logic.buy_product.make_a_purchase(
        user=user,
        product=product,
        finance_account=finance_account,
        broker=router.broker,
    )
