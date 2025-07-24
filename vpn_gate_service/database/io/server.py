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
