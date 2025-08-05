from aiogram.filters import BaseFilter
from aiogram.types import Message
import httpx

import config


class IsModeratorFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{config.settings.GATE_URL}/user/is_moderator",
                    json={"user_id": user_id},
                )
                resp_json = response.json()
                if resp_json.get("status") == "ok":
                    return resp_json.get("data", {}).get("is_moderator", False)
        except httpx.HTTPError as e:
            print(f"Moderator check failed: {e}")
        return False
