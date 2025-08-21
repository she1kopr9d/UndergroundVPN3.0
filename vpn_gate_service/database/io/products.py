import typing

import database.core
import database.models
import schemas.product
import schemas.telegram
import sqlalchemy
import sqlalchemy.orm


async def get_products_with_pagination(
    data: schemas.telegram.MarketPage,
) -> typing.Tuple[typing.List[schemas.product.ProductInfo], int]:
    async with database.core.async_session_factory() as session:
        stmt_count = sqlalchemy.select(sqlalchemy.func.count()).select_from(
            database.models.Product
        )
        count_result = await session.execute(stmt_count)
        total_count = count_result.scalar_one()
        max_page = max(
            (total_count + data.pagination - 1) // data.pagination, 1
        )
        stmt_products = (
            sqlalchemy.select(database.models.Product)
            .offset(data.page * data.pagination)
            .limit(data.pagination)
            .order_by(database.models.Product.created_at.desc())
        )
        result_products = await session.execute(stmt_products)
        products = result_products.scalars().all()
        return [
            schemas.product.ProductInfo(
                product_id=prod.id,
                product_name=prod.name,
            )
            for prod in products
        ], max_page


async def get_products_with_pagination_f(
    data: schemas.telegram.MarketPage,
    is_friend: bool,
) -> typing.Tuple[typing.List[schemas.product.ProductInfo], int]:
    async with database.core.async_session_factory() as session:
        stmt_count = sqlalchemy.select(sqlalchemy.func.count()).select_from(
            database.models.Product
        )
        if not is_friend:
            stmt_count = stmt_count.where(
                database.models.Product.is_friend == False
            )
        count_result = await session.execute(stmt_count)
        total_count = count_result.scalar_one()
        max_page = max(
            (total_count + data.pagination - 1) // data.pagination, 1
        )
        stmt_products = (
            sqlalchemy.select(database.models.Product)
            .offset(data.page * data.pagination)
            .limit(data.pagination)
            .order_by(database.models.Product.created_at.desc())
        )
        if not is_friend:
            stmt_products = stmt_products.where(
                database.models.Product.is_friend == False
            )
        result_products = await session.execute(stmt_products)
        products = result_products.scalars().all()
        return [
            schemas.product.ProductInfo(
                product_id=prod.id,
                product_name=prod.name,
            )
            for prod in products
        ], max_page
