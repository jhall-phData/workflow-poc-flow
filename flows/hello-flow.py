import prefect
from prefect import task, Flow
from flow_utils.prefect_configs import set_run_config,set_storage

@task(log_stdout=True)
def hello_task():
    logger = prefect.context.get("logger")
    logger.info("Hello world!")
    return True

# Flow Name must match the filename in Github
FLOW_NAME = "hello-flow"

with Flow(
    FLOW_NAME,
    #executor=LocalDaskExecutor(),
    storage=set_storage(FLOW_NAME),
    run_config=set_run_config(),
) as flow:
#with Flow("hello-flow") as flow:
    success = hello_task()