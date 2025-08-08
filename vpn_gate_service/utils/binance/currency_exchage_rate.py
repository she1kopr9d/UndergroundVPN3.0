import httpx


async def get_rub_to_usdt_binance() -> float:
    url = "https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    rub_per_usdt = float(data["price"])
    usdt_per_rub = 1 / rub_per_usdt
    return usdt_per_rub
