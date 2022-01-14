from prefect.run_configs import LocalRun, KubernetesRun, RunConfig
from prefect.storage.github import GitHub
from prefect.client.secrets import Secret


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
        path=f"flows/{flow_name}.py",
        access_token_secret="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"
    )