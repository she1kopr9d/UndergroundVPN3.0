import sqlalchemy

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
            name=server.name,
            code=server.secret_key
        )
        session.add(new_server)
        session.commit()
        session.refresh(new_server)
        return new_server
