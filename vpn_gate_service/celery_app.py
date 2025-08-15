import utils.acelery

import config
import rabbit


app = utils.acelery.AsyncCelery(
    "worker",
    broker=config.rabbitmq.rabbitmq_url,
    backend=config.celery.CELERY_RESULT_BACKEND,
    broker_instance=rabbit.broker,
)


import tasks # noqa


app.conf.beat_schedule = {
    "periodic-test-task": {
        "task": "tasks.periodic_task",
        "schedule": 10.0,
    },
}
app.conf.timezone = "UTC"
