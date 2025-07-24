import asyncio
import logging

import fastapi
from contextlib import asynccontextmanager

from app.schema import UserInput
from app.services import config_services
from app.ping import handshake_loop


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    print("Starting app initialization...")
    task = asyncio.create_task(handshake_loop())
    yield
    print("Preparing for app shutdown...")
    task.cancel()


app = fastapi.FastAPI(lifespan=lifespan)


@app.post("/user/add")
def add_user(user: UserInput):
    try:
        config = config_services.load_config()
        config_services.add_user_to_config(
            config, str(user.email), str(user.uuid)
        )
        config_services.save_config(config)
        return {"message": "Пользователь добавлен и Xray перезапущен"}
    except ValueError as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@app.post("/user/remove")
def remove_user(user: UserInput):
    try:
        config = config_services.load_config()
        config_services.remove_user_from_config(
            config, str(user.email), str(user.uuid)
        )
        config_services.save_config(config)
        return {"message": "Пользователь удалён и Xray перезапущен"}
    except ValueError as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))
