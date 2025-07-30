import fastapi

import routers.dev
import routers.user
import routers.servers
import routers.rabbit.user
import routers.rabbit.server


app = fastapi.FastAPI()
app.include_router(routers.dev.router)
app.include_router(routers.user.router)
app.include_router(routers.servers.router)
app.include_router(routers.rabbit.user.router)
app.include_router(routers.rabbit.server.router)
