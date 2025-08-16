import celery_app
import rabbit  # noqa


@celery_app.app.async_task_with_broker(name="tasks.exec_vpn_30_days")
async def exec_vpn_30_days(
    data: dict,
):
    pass


@celery_app.app.async_task_with_broker(name="tasks.remove_vpn_30_days")
async def remove_vpn_30_days(
    data: dict,
):
    pass
