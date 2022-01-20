import datetime
import requests

from prefect import task, Flow

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

from flow_utils.prefect_configs import set_run_config,set_storage

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
    return True

with Flow(
    FLOW_NAME,
    #executor=LocalDaskExecutor(),
    storage=set_storage(FLOW_NAME),
    run_config=set_run_config(),
) as flow:
    KVUri = "https://workflow-poc-kv001.vault.azure.net/"
    
    # this works if creds are env vars; but why
    credential = DefaultAzureCredential()    
    azclient = SecretClient(vault_url=KVUri, credential=credential)
    # SevenDwarfs = "https://cdn.touringplans.com/datasets/7_dwarfs_train.csv"
    retrieved_secret = azclient.get_secret("SevenDwarfsURL")
    print(f"Your secret is '{retrieved_secret.value}'.")

    reference_data = extract_data(retrieved_secret.value)
    success = load_reference_data(reference_data, credential)


  

