import requests
import prefect
from prefect import task, Flow

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
def load_reference_data(ref_data):
    print("saving reference data...")
    with open("7_dwarfs_train.csv", "wb") as f:
        f.write(ref_data)

def main():
    SevenDwarfs = "https://cdn.touringplans.com/datasets/7_dwarfs_train.csv"

    with Flow("7dwarfs") as flow:
        reference_data = extract_data(SevenDwarfs)
        transformed_live_data = transform(reference_data)
        load_reference_data(reference_data)

    #flow.run()


if __name__ == "__main__":
    main()