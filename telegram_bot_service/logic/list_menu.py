import rabbit


async def publish_list_menu(
    queue: str,
    user_id: int,
    message_id: int,
    page: int = 0,
    pagination: int = 3,
):
    await rabbit.broker.publish(
        {
            "user_id": user_id,
            "page": page,
            "pagination": pagination,
            "message_id": message_id,
        },
        queue=queue,
    )
