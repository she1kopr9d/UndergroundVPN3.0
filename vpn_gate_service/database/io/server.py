import typing

import database.core
import database.models
import schemas.servers
import sqlalchemy
import sqlalchemy.orm


async def get_low_server_id(servers_names: list[str]) -> str | None:
    async with database.core.async_session_factory() as session:
        stmt = (
            sqlalchemy.select(database.models.Server.name)
            .outerjoin(database.models.Config)
            .where(database.models.Server.name.in_(servers_names))
            .group_by(database.models.Server.id)
            .order_by(sqlalchemy.func.count(database.models.Config.id))
            .limit(1)
        )

        result = await session.execute(stmt)
        low_server_name: str | None = result.scalar_one_or_none()
        return low_server_name


def server_exists(server: schemas.servers.ServerAuth) -> bool:
    with database.core.session_factory() as session:
        stmt = sqlalchemy.select(database.models.Server).where(
            database.models.Server.name == server.name,
            database.models.Server.code == server.secret_key,
        )
        result = session.execute(stmt).scalar_one_or_none()
        return result is not None


def get_server_id_by_name(server_name: str) -> int | None:
    with database.core.session_factory() as session:
        stmt = sqlalchemy.select(database.models.Server.id).where(
            database.models.Server.name == server_name
        )
        result = session.execute(stmt).scalar_one_or_none()
        return result


def create_server(server: schemas.servers.ServerCreate):
    with database.core.session_factory() as session:
        new_server = database.models.Server(
            name=server.name, code=server.secret_key
        )
        session.add(new_server)
        session.commit()
        session.refresh(new_server)
        return new_server


def get_server_config_data(server_id: int):
    with database.core.session_factory() as session:
        stmt = (
            sqlalchemy.select(database.models.Server)
            .options(sqlalchemy.orm.joinedload(database.models.Server.config))
            .where(database.models.Server.id == server_id)
        )
        db_server = session.scalar(stmt)

        if db_server and db_server.config:
            return db_server.config.config_data
        return None


def create_server_config(
    server: database.models.Server,
    public_key: str,
    private_key: str,
    config_data: dict,
) -> database.models.ServerConfig:
    with database.core.session_factory() as session:
        server_config = database.models.ServerConfig(
            server_id=server.id,
            public_key=public_key,
            private_key=private_key,
            config_data=config_data,
        )
        session.add(server_config)
        session.commit()
        session.refresh(server_config)
        return server_config


def get_secret_key_by_name(name: str) -> str:
    with database.core.session_factory() as session:
        stmt = sqlalchemy.select(database.models.Server.code).where(
            database.models.Server.name == name
        )
        result = session.execute(stmt).scalar_one_or_none()
        return result


async def add_user_in_config(
    uuid: str,
    email: str,
    server_id: int,
    client_data_formatter: typing.Callable,
    client_add_executor: typing.Callable,
) -> None:
    client_data = client_data_formatter(
        uuid,
        email,
    )

    async with database.core.async_session_factory() as session:
        stmt: sqlalchemy.Select = sqlalchemy.select(
            database.models.ServerConfig
        ).where(database.models.ServerConfig.server_id == server_id)
        result = await session.execute(stmt)
        config_obj: database.models.ServerConfig | None = (
            result.scalar_one_or_none()
        )
        temp_config_data = config_obj.config_data.copy()
        client_add_executor(
            temp_config_data,
            client_data,
        )
        stmt: sqlalchemy.Select = (
            sqlalchemy.update(database.models.ServerConfig)
            .where(database.models.ServerConfig.server_id == server_id)
            .values(config_data=temp_config_data)
        )
        await session.execute(stmt)
        await session.commit()


async def delete_user_from_config(
    uuid: str,
    server_id: int,
    client_delete_executor: typing.Callable,
) -> None:
    async with database.core.async_session_factory() as session:
        stmt: sqlalchemy.Select = sqlalchemy.select(
            database.models.ServerConfig
        ).where(database.models.ServerConfig.server_id == server_id)
        result = await session.execute(stmt)
        config_obj: database.models.ServerConfig | None = (
            result.scalar_one_or_none()
        )

        if not config_obj:
            return

        temp_config_data = config_obj.config_data.copy()

        temp_config_data["inbounds"][0]["settings"]["clients"] = (
            client_delete_executor(
                temp_config_data,
                uuid,
            )
        )

        update_stmt = (
            sqlalchemy.update(database.models.ServerConfig)
            .where(database.models.ServerConfig.server_id == server_id)
            .values(config_data=temp_config_data)
        )
        await session.execute(update_stmt)
        await session.commit()
