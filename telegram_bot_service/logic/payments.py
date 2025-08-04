import httpx

import config
import rabbit


async def get_payment_methods(
    user_id: int,
) -> list:
    """
    {
        "status": "ok",
        "payment_methods":
        [
            {
                "title": "...",
                "method": "...",
            },
            ...,
        ],
    }
    """
    try:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(
                url=f"{config.settings.GATE_URL}/deposit/list",
                json={
                    "user_id": user_id,
                },
            )
            data = response.json()
            if data["status"] != "ok":
                return None
            return data
    except httpx.HTTPError as e:
        print(f"Get payment method failed: {e}")


async def create_payment(
    user_id: int,
    message_id: int,
    amount: int,
    method: str,
):
    await rabbit.broker.publish(
        {
            "user_id": user_id,
            "message_id": message_id,
            "amount": amount,
            "method": method,
        },
        queue="create_payment",
    )
