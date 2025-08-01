import fastapi
import faststream.rabbit.fastapi

import config
import schemas.config
import schemas.servers
import schemas.telegram
import logic.server_session
import logic.server_query
import logic.config_query
import database.io.server


router = faststream.rabbit.fastapi.RabbitRouter(config.rabbitmq.rabbitmq_url)


@router.subscriber("create_config")
async def handle_create_config(data: schemas.config.CreateConfig):
    print("create config")
    if not logic.server_session.is_authorized(data.server_name):
        raise fastapi.HTTPException(
            status_code=401, detail="This server is not active"
        )
    server = logic.server_session.get_active_server(data.server_name)

    config_url = await logic.server_query.create_config(
        create_data=data,
        server_data=server,
    )

    await router.broker.publish(
        {
            "user_id": data.user_id,
            "config_url": config_url,
        },
        queue="create_config_answer",
    )


@router.subscriber("create_server")
async def handle_create_server(data: schemas.telegram.CreateServerData):
    server = database.io.server.create_server(
        schemas.servers.ServerCreate(
            name=data.name,
            secret_key=data.secret_key,
        ),
    )

    server_config = await logic.config_query.create_server_config(
        server,
    )

    await router.broker.publish(
        {
            "user_id": data.user_id,
            "status": "ok",
        },
        queue="create_server_answer",
    )
