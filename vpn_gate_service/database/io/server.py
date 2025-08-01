import sqlalchemy
import sqlalchemy.orm

import database.database
import database.models
import schemas.servers


def server_exists(server: schemas.servers.ServerAuth) -> bool:
    with database.database.session_factory() as session:
        stmt = sqlalchemy.select(database.models.Server).where(
            database.models.Server.name == server.name,
            database.models.Server.code == server.secret_key,
        )
        result = session.execute(stmt).scalar_one_or_none()
        return result is not None


def get_server_id_by_name(server_name: str) -> int | None:
    with database.database.session_factory() as session:
        stmt = sqlalchemy.select(database.models.Server.id).where(
            database.models.Server.name == server_name
        )
        result = session.execute(stmt).scalar_one_or_none()
        return result


def create_server(server: schemas.servers.ServerCreate):
    with database.database.session_factory() as session:
        new_server = database.models.Server(
            name=server.name, code=server.secret_key
        )
        session.add(new_server)
        session.commit()
        session.refresh(new_server)
        return new_server


def get_server_config_data(server_id: int):
    with database.database.session_factory() as session:
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
    with database.database.session_factory() as session:
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
    with database.database.session_factory() as session:
        stmt = sqlalchemy.select(database.models.Server.code).where(
            database.models.Server.name == name
        )
        result = session.execute(stmt).scalar_one_or_none()
        return result
