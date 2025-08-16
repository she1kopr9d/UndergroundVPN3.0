import sqlalchemy

import datetime
import database.models
import database.core


async def create_subscription(
    user_id: int,
    product_id: int,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    payment_id: int,
) -> database.models.Subscription:
    async with database.core.async_session_factory() as session:
        subscription = database.models.Subscription(
            user_id=user_id,
            product_id=product_id,
            start_date=start_date,
            end_date=end_date,
            payment_id=payment_id,
            status=database.models.SubscriptionStatus.active,
        )
        session.add(subscription)
        await session.flush()
        charge = database.models.SubscriptionCharge(
            subscription_id=subscription.id,
            payment_id=payment_id,
        )
        session.add(charge)
        await session.commit()
        await session.refresh(subscription)
        return subscription


async def create_subscription_with_duration(
    user_id: int,
    product_id: int,
    days: int,
    payment_id: int,
) -> database.models.Subscription:
    now = datetime.datetime.utcnow()
    end_date = now + datetime.timedelta(days=days)
    return await create_subscription(
        user_id=user_id,
        product_id=product_id,
        start_date=now,
        end_date=end_date,
        payment_id=payment_id,
    )


async def extend_subscription(
    subscription_id: int,
    days: int,
    payment_id: int,
) -> database.models.Subscription:
    async with database.core.async_session_factory() as session:
        result = await session.execute(
            sqlalchemy.select(database.models.Subscription).where(
                database.models.Subscription.id == subscription_id
            )
        )
        subscription = result.scalar_one_or_none()
        if not subscription:
            raise ValueError(
                f"Subscription with id={subscription_id} not found"
            )
        base_date = max(subscription.end_date, datetime.datetime.utcnow())
        subscription.end_date = base_date + datetime.timedelta(days=days)
        subscription.status = database.models.SubscriptionStatus.active
        charge = database.models.SubscriptionCharge(
            subscription_id=subscription.id,
            payment_id=payment_id,
        )
        session.add(charge)
        await session.commit()
        await session.refresh(subscription)
        return subscription


async def get_subscriptions_expiring_in(days: int) -> list[int]:
    async with database.core.async_session_factory() as session:
        now = datetime.datetime.utcnow()
        expire_before = now + datetime.timedelta(days=days)
        result = await session.execute(
            sqlalchemy.select(database.models.Subscription.id).where(
                database.models.Subscription.status
                == database.models.SubscriptionStatus.active,
                database.models.Subscription.end_date <= expire_before,
            )
        )
        subscription_ids = [row[0] for row in result.all()]
        return subscription_ids


async def set_subscription_inactive(
    subscription_id: int,
    status: database.models.SubscriptionStatus = (
        database.models.SubscriptionStatus.expired
    ),
) -> database.models.Subscription:
    async with database.core.async_session_factory() as session:
        result = await session.execute(
            sqlalchemy.select(database.models.Subscription).where(
                database.models.Subscription.id == subscription_id
            )
        )
        subscription = result.scalar_one_or_none()
        if not subscription:
            raise ValueError(
                f"Subscription with id={subscription_id} not found"
            )
        subscription.status = status
        await session.commit()
        await session.refresh(subscription)
        return subscription


async def expire_overdue_subscriptions() -> list[database.models.Subscription]:
    async with database.core.async_session_factory() as session:
        now = datetime.datetime.utcnow()
        result = await session.execute(
            sqlalchemy.select(database.models.Subscription).where(
                database.models.Subscription.status
                == database.models.SubscriptionStatus.active,
                database.models.Subscription.end_date < now,
            )
        )
        expired_subs = result.scalars().all()
        if not expired_subs:
            return []
        for sub in expired_subs:
            sub.status = database.models.SubscriptionStatus.expired
        await session.commit()
        for sub in expired_subs:
            await session.refresh(sub)
        return expired_subs
