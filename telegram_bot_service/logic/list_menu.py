import aiogram.types
import rabbit


async def publish_list_menu(
    queue: str,
    user_id: int,
    message_id: int,
    page: int = 0,
    pagination: int = 5,
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


async def load_page_handler(
    message: aiogram.types.Message,
    queue: str,
):
    sent_message = await message.answer("Загружаю...")
    await publish_list_menu(
        queue=queue,
        user_id=message.from_user.id,
        message_id=sent_message.message_id,
    )


async def load_page_handler_bot(
    bot: aiogram.Bot,
    user_id: int,
    queue: str,
):
    send_message = await bot.send_message(
        chat_id=user_id,
        text="Загружаю...",
    )
    await publish_list_menu(
        queue=queue,
        user_id=user_id,
        message_id=send_message.message_id,
    )
