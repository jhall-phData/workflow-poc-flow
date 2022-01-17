import datetime
import requests
from prefect import task, Flow
from prefect.run_configs import LocalRun, KubernetesRun, RunConfig
from prefect.storage.github import GitHub

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings


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

FLOW_NAME = "azSevenDwarfs"

@task(log_stdout=True)
def extract_data(url):
    print("fetching reference data...")
    html = requests.get(url)
    if html.ok:
        return html.content
    else:
        raise ValueError("{} could not be retrieved.".format(url))

@task(log_stdout=True)
def transform(ref_data):
    print("cleaning & transform aircraft data...")
    live_aircraft_data = []
    return live_aircraft_data

@task(log_stdout=True)
def load_reference_data(ref_data, az_credential):
    print("saving reference data...")

    storage_account_name = "workflowpoc"
    service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
        "https", storage_account_name), credential=az_credential)
    file_system_client = service_client.get_file_system_client(file_system="raw")
    directory_client = file_system_client.get_directory_client("sevendwarfs")
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"7_dwarfs_train_{ts}.csv"
    print(f"Uploading file {filename}")
    file_client = directory_client.get_file_client(filename)
    file_client.upload_data(ref_data, overwrite=True)



    SevenDwarfs = "https://cdn.touringplans.com/datasets/7_dwarfs_train.csv"

    # with Flow("7dwarfs") as flow:
    #     reference_data = extract_data(SevenDwarfs)
    # #     transformed_live_data = transform(reference_data)
    #     load_reference_data(reference_data, credential)

    # flow.run()

with Flow(
    FLOW_NAME,
    #executor=LocalDaskExecutor(),
    storage=set_storage(FLOW_NAME),
    run_config=set_run_config(),
) as flow:
    KVUri = "https://workflow-poc-kv001.vault.azure.net/"
    
    credential = DefaultAzureCredential()    
    azclient = SecretClient(vault_url=KVUri, credential=credential)

    retrieved_secret = azclient.get_secret("SevenDwarfsURL")
    print(f"Your secret is '{retrieved_secret.value}'.")

    reference_data = extract_data(retrieved_secret.value)
    load_reference_data(reference_data, credential)


  

