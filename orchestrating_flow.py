from prefect import Flow
from prefect.tasks.prefect import StartFlowRun
from prefect.run_configs import LocalRun, KubernetesRun, RunConfig
from prefect.storage.github import GitHub

FLOW_NAME = "orchestrating_flow"
PROJECT_NAME = "dev-workflow-poc"
start_flow_run = StartFlowRun(project_name=PROJECT_NAME, wait=True)

def set_run_config(local: bool = False) -> RunConfig:
    if local:
        return LocalRun(labels=["dev"])
    return KubernetesRun(
        labels=["prefect"],
        image=f"prefecthq/prefect:latest",
        image_pull_policy="IfNotPresent",
    )


def set_storage(flow_name: str) -> GitHub:   
    return GitHub(
        repo="jhall-phData/workflow-poc-flow",
        path=f"{flow_name}.py",
        access_token_secret="GITHUB_ACCESS_TOKEN"
    )

with Flow(
    FLOW_NAME, storage=set_storage(FLOW_NAME), run_config=set_run_config(),
) as flow:
    kickoff_flow = start_flow_run(flow_name="azSevenDwarfs")
    
    