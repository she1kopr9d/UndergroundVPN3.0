import celery_app
import logic.server_query
import rabbit
import schemas.config
import schemas.servers


@celery_app.app.async_task_with_broker(name="tasks.create_config_task")
async def create_config_task(data: dict):
    user: schemas.config.CreateConfig = schemas.config.CreateConfig(
        **data["user"]
    )
    server: schemas.servers.ServerPublicInfo = (
        schemas.servers.ServerPublicInfo(**data["server"])
    )
    subscription_id: int | None = data.get("subscription_id", None)
    config_url = await logic.server_query.create_config(
        create_data=user,
        server_data=server,
        subscription_id=subscription_id,
    )

    await rabbit.broker.publish(
        {
            "user_id": user.user_id,
            "config_url": config_url,
        },
        queue="create_config_answer",
    )
