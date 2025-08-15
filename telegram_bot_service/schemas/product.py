import pydantic
import schemas.base


class ProductCellInfo(pydantic.BaseModel):
    product_id: int
    product_name: str


class ProductListData(
    schemas.base.BasePage,
    schemas.base.DefaultTelegramANSW,
):
    products: list[ProductCellInfo]


class ProductView(
    schemas.base.DefaultTelegramANSW,
    ProductCellInfo,
):
    page: int
    product_type: str
    product_price: float
    duration_days: int | None
