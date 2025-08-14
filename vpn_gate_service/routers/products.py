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
