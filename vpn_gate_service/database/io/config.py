import database.core
import database.models
import schemas.telegram


async def create_config(
    name: str,
    uuid: str,
    config: str,
    server_id: int,
    user_data: schemas.telegram.UserAllData,
) -> None:
    async with database.core.async_session_factory() as session:
        new_config = database.models.Config(
            name=name,
            uuid=uuid,
            config=config,
            server_id=server_id,
            user_id=user_data.id,
        )

        session.add(new_config)
        await session.commit()
        await session.refresh(new_config)
