import typing

import database.models
import pydantic
import schemas.base


class ProductShortSchema(pydantic.BaseModel):
    id: int
    name: typing.Optional[str]
    price: float
    product_type: database.models.ProductType

    model_config = pydantic.ConfigDict(from_attributes=True)


class ProductId(schemas.base.DefaultTelegramData):
    product_id: int


class ProductGet(ProductId):
    pass


class ProductGetPaggination(ProductId):
    page: int


class BuyProductData(ProductGet):
    pass


class ProductInfo(pydantic.BaseModel):
    product_id: int
    product_name: str


class ProductView(
    schemas.base.DefaultTelegramData,
    ProductInfo,
):
    page: int
    product_type: str
    product_price: float
    duration_days: int | None
