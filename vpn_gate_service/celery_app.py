import celery

import config


app = celery.Celery(
    "worker",
    broker=config.rabbitmq.rabbitmq_url,
    backend=config.celery.CELERY_RESULT_BACKEND,
)


import tasks


app.conf.beat_schedule = {
    "periodic-test-task": {
        "task": "tasks.periodic_task",
        "schedule": 10.0,
    },
}
app.conf.timezone = "UTC"
