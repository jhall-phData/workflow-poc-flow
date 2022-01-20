import prefect
from prefect import task, Flow

@task(log_stdout=True)
def hello_task():
    logger = prefect.context.get("logger")
    logger.info("Hello world!")
    return True

with Flow("hello-flow") as flow:
    success = hello_task()