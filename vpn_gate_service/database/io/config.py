import sqlalchemy

import database.core
import database.models

import schemas.telegram
import schemas.config


async def create_config(
    name: str,
    uuid: str,
    config: str,
    server_id: int,
    user_data: schemas.telegram.UserAllData,
) -> None:
    async with database.core.async_session_factory() as session:
        new_config = database.models.Config(
            name=name,
            uuid=uuid,
            config=config,
            server_id=server_id,
            user_id=user_data.id,
        )

        session.add(new_config)
        await session.commit()
        await session.refresh(new_config)


async def get_configs_with_pagination(
    data: schemas.telegram.ConfPage,
) -> tuple[list[schemas.config.ConfigInfo], int]:
    async with database.core.async_session_factory() as session:
        stmt_user = sqlalchemy.select(database.models.TelegramUser).where(
            database.models.TelegramUser.telegram_id == data.user_id
        )
        result = await session.execute(stmt_user)
        user = result.scalar_one_or_none()
        if not user:
            return [], 1
        stmt_count = sqlalchemy.select(sqlalchemy.func.count()).where(
            database.models.Config.user_id == user.id
        )
        count_result = await session.execute(stmt_count)
        total_count = count_result.scalar_one()
        max_page = max(
            (total_count + data.pagination - 1) // data.pagination, 1
        )
        stmt_configs = (
            sqlalchemy.select(database.models.Config)
            .where(database.models.Config.user_id == user.id)
            .offset(data.page * data.pagination)
            .limit(data.pagination)
            .order_by(database.models.Config.created_at.desc())
        )
        result_configs = await session.execute(stmt_configs)
        configs = result_configs.scalars().all()
        return [
            schemas.config.ConfigInfo(
                config_id=cfg.id,
                config_name=cfg.name,
            )
            for cfg in configs
        ], max_page
