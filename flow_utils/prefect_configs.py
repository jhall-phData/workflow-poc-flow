import prefect
from prefect.run_configs import LocalRun, KubernetesRun, RunConfig
from prefect.storage.github import GitHub



def set_run_config(local: bool = False) -> RunConfig:
    if local:
        return LocalRun(labels=["dev"])
    return KubernetesRun(
        labels=["prefect"],
        image=f"workflowpocacr001.azurecr.io/prefect-repo:latest",
        image_pull_policy="IfNotPresent",
    )


def set_storage(flow_name: str) -> GitHub:   
    return GitHub(
        repo="jhall-phData/workflow-poc-flow",
        path=f"flows/{flow_name}.py",
        access_token_secret="GITHUB_ACCESS_TOKEN"
    )