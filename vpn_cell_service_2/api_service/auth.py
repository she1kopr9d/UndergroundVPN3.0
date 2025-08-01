import asyncio
import httpx
import contextlib

import fastapi

import config
import xray


async def init_vpn():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.post(
                    f"{config.settings.gate_url}/server/auth",
                    json=config.settings.payload,
                    timeout=5,
                )
                resp.raise_for_status()
                print("Auth OK:", resp.json())
                data = resp.json()
                if data["status"] != "ok":
                    raise Exception("Authorizate status error")
                return data["config"]
            except Exception as e:
                print("Auth failed:", e)
                print("Next try before 5 second ....")
                await asyncio.sleep(5)


async def handshake_loop():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                resp = await client.post(
                    f"{config.settings.gate_url}/server/handshake",
                    json=config.settings.payload,
                    timeout=5,
                )
                resp.raise_for_status()
                print("Handshake OK:", resp.json())
            except Exception as e:
                print("Handshake failed:", e)
            await asyncio.sleep(5)


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    print("Starting app initialization...")
    config_data = await init_vpn()
    xray.raw_load_config(config_data)
    xray.restart_xray_container()
    task = asyncio.create_task(handshake_loop())
    yield
    print("Preparing for app shutdown...")
    task.cancel()
