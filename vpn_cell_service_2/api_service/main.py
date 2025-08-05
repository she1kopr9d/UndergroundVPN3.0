import auth
import fastapi
import routers.config

app = fastapi.FastAPI(lifespan=auth.lifespan)
app.include_router(routers.config.router)
