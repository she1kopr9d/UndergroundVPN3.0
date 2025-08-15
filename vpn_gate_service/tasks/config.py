import asyncio

import celery_app
import logic.server_query
import rabbit
import schemas.servers
import schemas.config


@celery_app.app.task(name="tasks.create_config_task")
def create_config_task(data: dict):
    async def _async_task():
        async with rabbit.broker:
            user: schemas.config.CreateConfig = (
                schemas.config.CreateConfig(**data["user"])
            )
            server: schemas.servers.ServerPublicInfo = (
                schemas.servers.ServerPublicInfo(**data["server"])
            )

            config_url = await logic.server_query.create_config(
                create_data=user,
                server_data=server,
            )

            await rabbit.broker.publish(
                {
                    "user_id": user.user_id,
                    "config_url": config_url,
                },
                queue="create_config_answer",
            )
    asyncio.run(_async_task())
