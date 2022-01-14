import prefect
from prefect import Flow
from prefect.tasks.prefect import StartFlowRun
from flow_utils.prefect_configs import set_run_config, set_storage

FLOW_NAME = "orchestrating_flow"
PROJECT_NAME = "dev-workflow-poc"
start_flow_run = StartFlowRun(project_name=PROJECT_NAME, wait=True)

prefect.context.setdefault("secrets", {}) # to make sure context has a secrets attribute
prefect.context.secrets["GITHUB_ACCESS_TOKEN"] = "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"

with Flow(
    FLOW_NAME, storage=set_storage(FLOW_NAME), run_config=set_run_config(),
) as flow:
    kickoff_flow = start_flow_run(flow_name="azSevenDwarfs")
    