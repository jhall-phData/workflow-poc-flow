from prefect import Flow
from prefect.tasks.prefect import StartFlowRun
from prefect_configs import set_run_config, set_storage

FLOW_NAME = "orchestrating_flow"
PROJECT_NAME = "dev-workflow-poc"
start_flow_run = StartFlowRun(project_name=PROJECT_NAME, wait=True)

with Flow(
    FLOW_NAME, storage=set_storage(FLOW_NAME), run_config=set_run_config(),
) as flow:
    kickoff_flow = start_flow_run(flow_name="azSevenDwarfs")
    