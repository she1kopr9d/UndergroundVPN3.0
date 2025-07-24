import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.orm

import config


sync_engine = sqlalchemy.create_engine(
    url=config.database.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

async_engine = sqlalchemy.ext.asyncio.create_async_engine(
    url=config.database.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

session_factory = sqlalchemy.orm.sessionmaker(sync_engine)

async_session_factory = sqlalchemy.ext.asyncio.async_sessionmaker(
    async_engine,
)
