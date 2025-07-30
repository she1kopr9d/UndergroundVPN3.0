import typing
import datetime

import sqlalchemy
import sqlalchemy.orm

import database.core


intpk = typing.Annotated[int, sqlalchemy.orm.mapped_column(primary_key=True)]
created_at = typing.Annotated[
    datetime.datetime,
    sqlalchemy.orm.mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())")
    ),
]
updated_at = typing.Annotated[
    datetime.datetime,
    sqlalchemy.orm.mapped_column(
        server_default=sqlalchemy.text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id: sqlalchemy.orm.Mapped[intpk]
    telegram_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        unique=True,
        nullable=False,
    )
    is_admin = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
    )
    username = sqlalchemy.Column(sqlalchemy.String)
    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    configs: sqlalchemy.orm.Mapped[list["Config"]] = (
        sqlalchemy.orm.relationship(
            back_populates="user", cascade="all, delete-orphan"
        )
    )


class Server(Base):
    __tablename__ = "servers"

    id: sqlalchemy.orm.Mapped[intpk]
    name = sqlalchemy.Column(sqlalchemy.String)
    code = sqlalchemy.Column(sqlalchemy.String)

    configs: sqlalchemy.orm.Mapped[list["Config"]] = (
        sqlalchemy.orm.relationship(
            back_populates="server", cascade="all, delete-orphan"
        )
    )


class Config(Base):
    __tablename__ = "configs"

    id: sqlalchemy.orm.Mapped[intpk]
    name = sqlalchemy.Column(sqlalchemy.String)
    uuid = sqlalchemy.Column(sqlalchemy.String)
    config = sqlalchemy.Column(sqlalchemy.String)

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    # server
    server_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("servers.id"),
    )

    server: sqlalchemy.orm.Mapped["Server"] = sqlalchemy.orm.relationship(
        back_populates="configs",
    )

    # user
    user_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("telegram_users.id"),
    )

    user: sqlalchemy.orm.Mapped["TelegramUser"] = sqlalchemy.orm.relationship(
        back_populates="configs",
    )
