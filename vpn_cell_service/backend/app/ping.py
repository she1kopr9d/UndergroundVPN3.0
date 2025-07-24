import asyncio
import httpx
from app.config import settings


async def handshake_loop():
    payload = {
        "name": settings.SERVER_NAME,
        "ip": settings.IP_ADDRESS,
        "port": settings.PORT,
        "api_version": settings.GATE_API_VERSION,
        "secret_key": settings.GATE_SECRET_KEY,
    }
    gate_url = f"http://{settings.GATE_IP_ADDRESS}:8000"

    async with httpx.AsyncClient() as client:
        # Первая авторизация
        try:
            resp = await client.post(
                f"{gate_url}/server/auth", json=payload, timeout=5
            )
            resp.raise_for_status()
            print("Auth OK:", resp.json())
        except Exception as e:
            print("Auth failed:", e)

        # Периодические хендшейки
        while True:
            try:
                resp = await client.post(
                    f"{gate_url}/server/handshake", json=payload, timeout=5
                )
                resp.raise_for_status()
                print("Handshake OK:", resp.json())
            except Exception as e:
                print("Handshake failed:", e)

            await asyncio.sleep(5)
