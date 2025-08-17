import datetime
import enum
import typing

import sqlalchemy
import sqlalchemy.orm

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
    is_handle = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
        server_default=sqlalchemy.false(),
    )
    username = sqlalchemy.Column(sqlalchemy.String)
    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    referrer_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("telegram_users.id"),
        nullable=True,
    )

    configs: sqlalchemy.orm.Mapped[list["Config"]] = (
        sqlalchemy.orm.relationship(
            back_populates="user", cascade="all, delete-orphan"
        )
    )

    referrer: sqlalchemy.orm.Mapped["TelegramUser"] = (
        sqlalchemy.orm.relationship(
            back_populates="referrals",
            remote_side="TelegramUser.id",
        )
    )

    referrals: sqlalchemy.orm.Mapped[list["TelegramUser"]] = (
        sqlalchemy.orm.relationship(
            back_populates="referrer",
            cascade="all, delete-orphan",
        )
    )

    finance_account = sqlalchemy.orm.relationship(
        "FinanceAccount",
        back_populates="user",
        uselist=False,
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

    config = sqlalchemy.orm.relationship(
        "ServerConfig",
        back_populates="server",
        uselist=False,
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


class ServerConfig(Base):
    __tablename__ = "server_configs"

    id: sqlalchemy.orm.Mapped[intpk]
    public_key: sqlalchemy.orm.Mapped[str]
    private_key: sqlalchemy.orm.Mapped[str]
    config_data: sqlalchemy.orm.Mapped[dict] = sqlalchemy.orm.mapped_column(
        sqlalchemy.JSON
    )
    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    # server
    server_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("servers.id"),
        unique=True,
    )
    server = sqlalchemy.orm.relationship(
        "Server",
        back_populates="config",
        uselist=False,
    )


class FinanceAccount(Base):
    __tablename__ = "finance_accounts"

    id: sqlalchemy.orm.Mapped[intpk]
    balance: sqlalchemy.orm.Mapped[float] = sqlalchemy.Column(
        sqlalchemy.Float, default=0.0, nullable=False
    )
    referral_percent: sqlalchemy.orm.Mapped[int] = sqlalchemy.Column(
        sqlalchemy.Integer,
        default=15,
        nullable=False,
    )
    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    # user
    user_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("telegram_users.id"),
    )

    user = sqlalchemy.orm.relationship(
        "TelegramUser",
        back_populates="finance_account",
        uselist=False,
    )

    payments: sqlalchemy.orm.Mapped[list["Payment"]] = (
        sqlalchemy.orm.relationship(
            back_populates="finance_account", cascade="all, delete-orphan"
        )
    )


class PaymentStatus(enum.Enum):
    pending = "pending"
    moderation = "moderation"
    completed = "completed"
    failed = "failed"


class PaymentMode(enum.Enum):
    test = "test"
    production = "production"


class PaymentMethod(enum.Enum):
    crypto = "crypto"
    telegram_star = "telegram_star"
    handle = "handle"
    system = "system"


class TransactionType(enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"


class Payment(Base):
    __tablename__ = "payments"

    id: sqlalchemy.orm.Mapped[intpk]
    amount: sqlalchemy.orm.Mapped[float]
    transaction_type: sqlalchemy.orm.Mapped[TransactionType] = (
        sqlalchemy.orm.mapped_column(
            sqlalchemy.Enum(TransactionType),
            nullable=False,
        )
    )
    status: sqlalchemy.orm.Mapped[PaymentStatus] = (
        sqlalchemy.orm.mapped_column(
            sqlalchemy.Enum(PaymentStatus),
            default=PaymentStatus.pending,
            nullable=False,
        )
    )
    mode: sqlalchemy.orm.Mapped[PaymentMode] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Enum(PaymentMode),
        default=PaymentMode.production,
        nullable=False,
    )
    payment_method: sqlalchemy.orm.Mapped[PaymentMethod] = (
        sqlalchemy.orm.mapped_column(
            sqlalchemy.Enum(PaymentMethod),
            nullable=False,
        )
    )

    external_id: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        sqlalchemy.String, nullable=True, unique=True
    )

    note: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Text,
        nullable=True,
    )

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    finance_account_id: sqlalchemy.orm.Mapped[int] = (
        sqlalchemy.orm.mapped_column(
            sqlalchemy.ForeignKey("finance_accounts.id")
        )
    )

    finance_account: sqlalchemy.orm.Mapped["FinanceAccount"] = (
        sqlalchemy.orm.relationship(
            back_populates="payments",
        )
    )


class Moderator(Base):
    __tablename__ = "moderators"

    id: sqlalchemy.orm.Mapped[intpk]

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    # user
    user_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("telegram_users.id"),
        unique=True,
    )


class PaymentReceipt(Base):
    __tablename__ = "payment_receipts"

    id: sqlalchemy.orm.Mapped[intpk]
    file_path: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        sqlalchemy.String, nullable=False
    )
    filename: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        sqlalchemy.String, nullable=False
    )

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    payment_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("payments.id"), nullable=False
    )


class ProductType(str, enum.Enum):
    one_time = "one_time"
    recurring = "recurring"


class Product(Base):
    __tablename__ = "products"

    id: sqlalchemy.orm.Mapped[intpk]
    name: sqlalchemy.orm.Mapped[typing.Optional[str]]
    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    duration_days: sqlalchemy.orm.Mapped[typing.Optional[int]]
    product_type = sqlalchemy.Column(
        sqlalchemy.Enum(ProductType),
        default=ProductType.recurring,
        nullable=False,
    )

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]


class SubscriptionStatus(str, enum.Enum):
    active = "active"
    expired = "expired"
    canceled = "canceled"


class SubscriptionCharge(Base):
    __tablename__ = "subscription_charges"

    id: sqlalchemy.orm.Mapped[intpk]

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    subscription_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("subscriptions.id"), nullable=False
    )
    subscription: sqlalchemy.orm.Mapped["Subscription"] = (
        sqlalchemy.orm.relationship(back_populates="charges")
    )
    payment_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("payments.id"),
    )
    payment: sqlalchemy.orm.Mapped["Payment"] = sqlalchemy.orm.relationship()


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: sqlalchemy.orm.Mapped[intpk]
    start_date: sqlalchemy.orm.Mapped[datetime.datetime]
    end_date: sqlalchemy.orm.Mapped[datetime.datetime]
    status: sqlalchemy.orm.Mapped[SubscriptionStatus] = (
        sqlalchemy.orm.mapped_column(
            sqlalchemy.Enum(SubscriptionStatus),
            default=SubscriptionStatus.active,
            nullable=False,
        )
    )

    created_at: sqlalchemy.orm.Mapped[created_at]
    updated_at: sqlalchemy.orm.Mapped[updated_at]

    product_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("products.id"), nullable=False
    )

    user_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("telegram_users.id"), nullable=False
    )
    user: sqlalchemy.orm.Mapped["TelegramUser"] = sqlalchemy.orm.relationship()

    payment_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("payments.id"), nullable=True
    )

    charges: sqlalchemy.orm.Mapped[list["SubscriptionCharge"]] = (
        sqlalchemy.orm.relationship(
            back_populates="subscription", cascade="all, delete-orphan"
        )
    )

    external_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.Integer, nullable=True, unique=True
    )


class ExecuteProduct(Base):
    __tablename__ = "execute_products"

    id: sqlalchemy.orm.Mapped[intpk]

    executor_name: sqlalchemy.orm.Mapped[str]

    product_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        sqlalchemy.ForeignKey("products.id"),
    )
