import settings.rabbitmq
import settings.server
import settings.database
import settings.xray


server = settings.server.Settings()
database = settings.database.Settings()
rabbitmq = settings.rabbitmq.Settings()
xray = settings.xray.Settings()
