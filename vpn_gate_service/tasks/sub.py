import celery_app
import database.io.base
import database.io.sub
import database.models
import logic.sub
import rabbit


async def check_day_sub(
    day: int,
    text: str,
):
    subs_ids: list[int] = (
        await database.io.sub.get_subscriptions_expiring_between(
            days_from=day - 1,
            days_to=day,
        )
    )
    if len(subs_ids) == 0:
        return
    users_ids: list[int] = await database.io.base.get_values_by_field_list(
        search_field=database.models.Subscription.id,
        values_fields=subs_ids,
        get_values_field=database.models.Subscription.user_id,
    )
    telegram_ids: list[int] = await database.io.base.get_values_by_field_list(
        search_field=database.models.TelegramUser.id,
        values_fields=users_ids,
        get_values_field=database.models.TelegramUser.telegram_id,
    )
    for telegram_id in telegram_ids:
        await rabbit.broker.publish(
            {
                "user_id": telegram_id,
                "text": text,
                "photo": None,
            },
            queue="send_telegram_message",
        )


@celery_app.app.async_task_with_broker(name="tasks.check_5_day_sub")
async def check_5_day_sub():
    print("[PEREODIC TASK] check_5_day_sub")
    await check_day_sub(
        day=5,
        text=(
            "Срок пользование подпиской заканчивается через 5 дней, "
            "если на вашем счете есть досаточно деняг, "
            "то сумма автоматически спишется и продлит срок."
        ),
    )


@celery_app.app.async_task_with_broker(name="tasks.check_3_day_sub")
async def check_3_day_sub():
    print("[PEREODIC TASK] check_3_day_sub")
    await check_day_sub(
        day=3,
        text=(
            "Срок пользование подпиской заканчивается через 3 дня, "
            "если на вашем счете есть досаточно деняг, "
            "то сумма автоматически спишется и продлит срок."
        ),
    )


@celery_app.app.async_task_with_broker(name="tasks.check_desub")
async def check_desub():
    print("[PEREODIC TASK] check_desub")
    subs_ids: list[int] = (
        await database.io.sub.get_expired_active_subscriptions()
    )
    for sub_id in subs_ids:
        await logic.sub.update_sub(sub_id)
