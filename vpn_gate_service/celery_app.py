import config
import rabbit
import utils.acelery

app = utils.acelery.AsyncCelery(
    "worker",
    broker=config.rabbitmq.rabbitmq_url,
    backend=config.rabbitmq.rabbitmq_url,
    broker_instance=rabbit.broker,
)

import tasks  # noqa

app.conf.beat_schedule = {
    "check_5_day_sub": {
        "task": "tasks.check_5_day_sub",
        "schedule": 60.0 * 60.0 * 24.0,
    },
    "check_3_day_sub": {
        "task": "tasks.check_3_day_sub",
        "schedule": 60.0 * 60.0 * 24.0,
    },
    "check_desub": {
        "task": "tasks.check_desub",
        "schedule": 10.0,
    },
    "deactivate_sub": {
        "task": "tasks.deactivate_sub",
        "schedule": 10.0,
    },
}
app.conf.timezone = "UTC"
