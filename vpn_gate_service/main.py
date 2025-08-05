import fastapi

import routers.dev
import routers.user
import routers.servers
import routers.deposite
import routers.rabbit.user
import routers.rabbit.server
import routers.rabbit.deposite
import routers.rabbit.moderator


app = fastapi.FastAPI()
app.include_router(routers.dev.router)
app.include_router(routers.user.router)
app.include_router(routers.servers.router)
app.include_router(routers.deposite.router)
app.include_router(routers.rabbit.user.router)
app.include_router(routers.rabbit.server.router)
app.include_router(routers.rabbit.deposite.router)
app.include_router(routers.rabbit.moderator.router)
