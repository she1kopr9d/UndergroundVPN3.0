import typing

import database.core
import database.models
import sqlalchemy
import sqlalchemy.orm


async def get_object_by_id(
    id: int,
    object_class: type[database.models.Base],
) -> database.models.Base | None:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(object_class).where(object_class.id == id)
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()
        return obj


async def delete_object_by_id(
    id: int,
    object_class: type[database.models.Base],
) -> bool:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(object_class).where(object_class.id == id)
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()

        if obj:
            await session.delete(obj)
            await session.commit()
            return True

        return False


async def get_object_by_field(
    field,
    value,
    object_class: type[database.models.Base],
) -> database.models.Base | None:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(object_class).where(value == field)
        result = await session.execute(stmt)
        obj = result.scalar_one_or_none()
        return obj


async def get_all_objects(
    object_class: type[database.models.Base],
) -> list[database.models.Base] | None:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(object_class)
        result = await session.execute(stmt)
        objects = result.scalars().all()
        return objects


async def get_all_objects_with_filter(
    object_class: type[database.models.Base],
    filters: dict[str, typing.Any] | None = None,
) -> list[database.models.Base] | None:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(object_class)
        if filters:
            for field, value in filters.items():
                stmt = stmt.where(getattr(object_class, field) == value)
        result = await session.execute(stmt)
        objects = result.scalars().all()
        return objects


async def update_field(
    object_class: type[database.models.Base],
    search_field,
    search_value,
    update_list,
) -> database.models.Base:
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.update(object_class)
            .where(search_field == search_value)
            .values(**update_list)
            .returning(object_class)
        )
        result = await session.execute(stmt)
        obj = result.scalar_one()
        await session.commit()
        await session.refresh(obj)
        return obj


async def get_all_field_list(
    object_class: type[database.models.Base],
    field,
) -> list[typing.Any]:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(field).select_from(object_class)
        result = await session.execute(stmt)
        values = result.scalars().all()
        return list(values)


async def get_values_by_field_list(
    search_field,
    values_fields: list[typing.Any],
    get_values_field,
) -> list[typing.Any]:
    async with database.core.async_session_factory() as session:
        stmt = sqlalchemy.select(get_values_field).where(
            search_field.in_(values_fields)
        )
        result = await session.execute(stmt)
        values = result.scalars().all()
        return list(values)
