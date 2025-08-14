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


class BuyProductData(schemas.base.DefaultTelegramData):
    product_id: int


class ProductInfo(pydantic.BaseModel):
    product_id: int
    product_name: str
