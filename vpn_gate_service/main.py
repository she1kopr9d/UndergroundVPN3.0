import fastapi
import routers.deposite
import routers.dev
import routers.products
import routers.rabbit.deposite
import routers.rabbit.market
import routers.rabbit.moderator
import routers.rabbit.products
import routers.rabbit.server
import routers.rabbit.user
import routers.servers
import routers.user

app = fastapi.FastAPI()
app.include_router(routers.deposite.router)
app.include_router(routers.dev.router)
app.include_router(routers.products.router)
app.include_router(routers.rabbit.deposite.router)
app.include_router(routers.rabbit.market.router)
app.include_router(routers.rabbit.moderator.router)
app.include_router(routers.rabbit.products.router)
app.include_router(routers.rabbit.server.router)
app.include_router(routers.rabbit.user.router)
app.include_router(routers.servers.router)
app.include_router(routers.user.router)
