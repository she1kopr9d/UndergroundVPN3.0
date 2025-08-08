import pydantic
import typing

import database.models

import schemas.base


class ProductShortSchema(pydantic.BaseModel):
    id: int
    name: typing.Optional[str]
    price: float
    product_type: database.models.ProductType

    model_config = pydantic.ConfigDict(from_attributes=True)


class BuyProductData(schemas.base.DefaultTelegramData):
    product_id: int
