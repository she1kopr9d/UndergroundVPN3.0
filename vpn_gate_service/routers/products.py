import config
import database.io.base
import database.models
import faststream.rabbit.fastapi
import schemas.product

router = faststream.rabbit.fastapi.RabbitRouter(
    url=config.rabbitmq.rabbitmq_url,
)


@router.post("/market/list")
async def market_list_router():
    objects: list[database.models.Product] = (
        await database.io.base.get_all_objects(database.models.Product)
    )
    return {
        "status": "ok",
        "products": [
            schemas.product.ProductShortSchema.model_validate(obj)
            for obj in objects
        ],
    }


@router.post("/market/list-a/{user_id}")
async def market_list_a_router(user_id):
    user: database.models.TelegramUser = (
        await database.io.base.get_object_by_field(
            field=database.models.TelegramUser.telegram_id,
            value=user_id,
            object_class=database.models.TelegramUser,
        )
    )
    filters = dict()
    if not user.is_friend:
        filters.update(
            {
                "is_friend": False,
            }
        )
    objects: list[database.models.Product] = (
        await database.io.base.get_all_objects_with_filter(
            object_class=database.models.Product,
            filters=filters,
        )
    )
    objects_f = []
    if not user.is_trial:
        print("Filtering trial products")
        for obj in objects:
            print(obj.price, obj.price > 0)
            if obj.price > 0:
                objects_f.append(obj)
    else:
        objects_f = objects

    return {
        "status": "ok",
        "products": [
            schemas.product.ProductShortSchema.model_validate(obj)
            for obj in objects_f
        ],
    }
