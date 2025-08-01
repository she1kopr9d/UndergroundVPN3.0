import fastapi

import schemas
import xray


router = fastapi.APIRouter()


@router.post("/user/add")
async def add_config_router(data: schemas.ConfigEditInfo):
    config_obj = xray.load_config()
    status = xray.add_user_to_config(data.client_data, config_obj)
    xray.save_config(config_obj)
    return {"status": status}


@router.post("/user/remove")
async def remove_config_router(data: schemas.ConfigEditInfo):
    config_obj = xray.load_config()
    status = xray.remove_user_from_config(data.client_data, config_obj)
    xray.save_config(config_obj)
    return {"status": status}
