import sqlalchemy
import sqlalchemy.orm

import database.core
import database.models


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
