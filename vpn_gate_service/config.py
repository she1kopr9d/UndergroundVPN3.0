import settings.celery
import settings.crypto
import settings.database
import settings.payment
import settings.rabbitmq
import settings.server
import settings.xray

celery = settings.celery.Settings()
database = settings.database.Settings()
payment = settings.payment.Settings()
rabbitmq = settings.rabbitmq.Settings()
server = settings.server.Settings()
xray = settings.xray.Settings()
crypto = settings.crypto.Settings()
