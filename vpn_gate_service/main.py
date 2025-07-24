import fastapi

import routers.servers
import routers.rabbit.user


app = fastapi.FastAPI()
app.include_router(routers.servers.router)
app.include_router(routers.rabbit.user.router)
