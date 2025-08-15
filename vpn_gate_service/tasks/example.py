import celery_app


@celery_app.app.task
def test_task(x, y):
    print(f"Running test_task: {x} + {y}")
    return x + y


@celery_app.app.task(name="tasks.periodic_task")
def periodic_task():
    print("Running periodic task every 10 seconds")
